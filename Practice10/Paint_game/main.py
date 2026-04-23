import pygame
import math

# Класс для создания кнопок интерфейса
class Button:
    def __init__(self, x, y, width, height, text, action_type, action_value, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_type = action_type # 'tool' (инструмент) или 'color' (цвет)
        self.action_value = action_value
        self.color = color

    def draw(self, surface, font, is_active):
        # Если кнопка активна, делаем ее фон темнее (или обводку толще)
        bg_color = (150, 150, 150) if is_active and self.action_type == 'tool' else self.color
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Рисуем обводку (белую, если выбрана, иначе черную)
        border_color = (255, 255, 255) if is_active else (0, 0, 0)
        pygame.draw.rect(surface, border_color, self.rect, 3 if is_active else 1)
        
        # Рисуем текст, если он есть
        if self.text:
            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Visual Pygame Paint")
    font = pygame.font.SysFont(None, 24)
    
    # Высота панели инструментов
    toolbar_height = 60
    
    # Холст теперь немного меньше, чтобы освободить место под меню сверху
    canvas = pygame.Surface((screen_width, screen_height - toolbar_height))
    canvas.fill((255, 255, 255)) # Пусть фон будет белым, как лист бумаги
    
    clock = pygame.time.Clock()
    
    # Текущие настройки
    current_color = (255, 0, 0)
    current_mode = 'line'
    radius = 5
    
    drawing = False
    start_pos = None
    last_pos = None

    # Создаем наши кнопки
    buttons = [
        # Инструменты
        Button(10, 10, 80, 40, "Line", 'tool', 'line'),
        Button(100, 10, 80, 40, "Rect", 'tool', 'rect'),
        Button(190, 10, 80, 40, "Circle", 'tool', 'circle'),
        Button(280, 10, 80, 40, "Eraser", 'tool', 'eraser'),
        
        # Цвета (без текста, просто цветные квадраты)
        Button(400, 10, 40, 40, "", 'color', (255, 0, 0), color=(255, 0, 0)),     # Красный
        Button(450, 10, 40, 40, "", 'color', (0, 255, 0), color=(0, 255, 0)),     # Зеленый
        Button(500, 10, 40, 40, "", 'color', (0, 0, 255), color=(0, 0, 255)),     # Синий
        Button(550, 10, 40, 40, "", 'color', (0, 0, 0), color=(0, 0, 0)),         # Черный
    ]

    while True:
        # --- 1. ОБРАБОТКА СОБЫТИЙ ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Левая кнопка мыши
                    # Проверяем, кликнули ли мы по кнопке в меню
                    if event.pos[1] < toolbar_height:
                        for btn in buttons:
                            if btn.rect.collidepoint(event.pos):
                                if btn.action_type == 'tool':
                                    current_mode = btn.action_value
                                elif btn.action_type == 'color':
                                    current_color = btn.action_value
                    else:
                        # Если кликнули ниже меню — начинаем рисовать
                        drawing = True
                        # Корректируем координаты мыши для холста (вычитаем высоту меню)
                        canvas_pos = (event.pos[0], event.pos[1] - toolbar_height)
                        start_pos = canvas_pos
                        last_pos = canvas_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    canvas_pos = (event.pos[0], event.pos[1] - toolbar_height)
                    if current_mode == 'rect':
                        draw_my_rect(canvas, current_color, start_pos, canvas_pos)
                    elif current_mode == 'circle':
                        draw_my_circle(canvas, current_color, start_pos, canvas_pos)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    canvas_pos = (event.pos[0], event.pos[1] - toolbar_height)
                    if current_mode == 'line':
                        pygame.draw.line(canvas, current_color, last_pos, canvas_pos, radius * 2)
                        last_pos = canvas_pos
                    elif current_mode == 'eraser':
                        pygame.draw.line(canvas, (255, 255, 255), last_pos, canvas_pos, radius * 6)
                        last_pos = canvas_pos

        # --- 2. ОТРИСОВКА ---
        screen.fill((200, 200, 200)) # Цвет панели инструментов (серый)
        
        # Рисуем холст (смещаем его вниз на toolbar_height)
        screen.blit(canvas, (0, toolbar_height)) 
        
        # Рисуем предпросмотр фигур прямо на экране поверх холста
        if drawing and start_pos:
            mouse_pos = pygame.mouse.get_pos()
            # Нужно вернуть координаты к экранным для предпросмотра
            screen_start = (start_pos[0], start_pos[1] + toolbar_height)
            if current_mode == 'rect':
                draw_my_rect(screen, current_color, screen_start, mouse_pos, width=2)
            elif current_mode == 'circle':
                draw_my_circle(screen, current_color, screen_start, mouse_pos, width=2)

        # Рисуем кнопки меню
        for btn in buttons:
            is_active = (btn.action_value == current_mode) or (btn.action_value == current_color)
            btn.draw(screen, font, is_active)

        pygame.display.flip()
        clock.tick(60)

# --- Вспомогательные функции ---

def draw_my_rect(surface, color, start, end, width=0):
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surface, color, (x, y, w, h), width)

def draw_my_circle(surface, color, start, end, width=0):
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    if radius > 0:
        pygame.draw.circle(surface, color, start, radius, width)

if __name__ == "__main__":
    main()