import pygame
import datetime
from tools import flood_fill, get_rect, get_distance

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint Application - TSIS 2")
    
    colors = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'black':(0,0,0), 'white':(255,255,255)}
    current_color = colors['black']
    mode = 'pencil'
    drawing = False
    size = 2
    
    canvas = pygame.Surface((800, 600))
    canvas.fill(colors['white'])
    ui_rect = pygame.Rect(0, 0, 800, 50)
    
    btns = {
        'red': pygame.Rect(10, 10, 30, 30),
        'green': pygame.Rect(50, 10, 30, 30),
        'blue': pygame.Rect(90, 10, 30, 30),
        'black': pygame.Rect(130, 10, 30, 30),
        'pencil': pygame.Rect(170, 10, 60, 30),
        'line': pygame.Rect(240, 10, 60, 30),
        'rect': pygame.Rect(310, 10, 60, 30),
        'circle': pygame.Rect(380, 10, 60, 30),
        'erase': pygame.Rect(450, 10, 60, 30),
        'fill': pygame.Rect(520, 10, 60, 30),
        'text': pygame.Rect(590, 10, 60, 30),
    }

    font = pygame.font.SysFont("Arial", 32)
    ui_font = pygame.font.SysFont("Arial", 14)
    
    start_pos = None
    last_pos = None
    clock = pygame.time.Clock()
    
    typing = False
    text_input = ""
    text_pos = (0,0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Клавиатура ---
            if event.type == pygame.KEYDOWN:
                # Изменение размера кисти
                if event.key == pygame.K_1: size = 2
                elif event.key == pygame.K_2: size = 5
                elif event.key == pygame.K_3: size = 10
                
                # Сохранение Ctrl + S
                elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    fname = f"paint_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    pygame.image.save(canvas, fname)
                    print(f"Canvas saved as {fname}")

                # Ввод текста
                if typing:
                    if event.key == pygame.K_RETURN:
                        t = font.render(text_input, True, current_color)
                        canvas.blit(t, text_pos)
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing = False
                        text_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        text_input += event.unicode
                        
            # --- Мышь ---
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[1] <= 50: # Клик по UI панели
                    for k, r in btns.items():
                        if r.collidepoint(event.pos):
                            if k in colors: current_color = colors[k]
                            else: mode = k
                else: # Клик по холсту
                    if mode == 'text':
                        if typing: # Зафиксировать предыдущий текст
                            t = font.render(text_input, True, current_color)
                            canvas.blit(t, text_pos)
                        typing = True
                        text_pos = event.pos
                        text_input = ""
                    elif mode == 'fill':
                        flood_fill(canvas, event.pos, current_color)
                        typing = False
                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos
                        typing = False

            if event.type == pygame.MOUSEBUTTONUP:
                if drawing:
                    drawing = False
                    if start_pos and mode in ['rect', 'circle', 'line']:
                        if mode == 'rect':
                            pygame.draw.rect(canvas, current_color, get_rect(start_pos, event.pos), size)
                        elif mode == 'circle':
                            radius = get_distance(start_pos, event.pos)
                            pygame.draw.circle(canvas, current_color, start_pos, radius, size)
                        elif mode == 'line':
                            pygame.draw.line(canvas, current_color, start_pos, event.pos, size)
                start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'pencil':
                        pygame.draw.line(canvas, current_color, last_pos, event.pos, size)
                        last_pos = event.pos
                    elif mode == 'erase':
                        pygame.draw.circle(canvas, colors['white'], event.pos, size * 5)
                        
        # --- Отрисовка ---
        screen.blit(canvas, (0, 0))
        
        # Предпросмотр текста в реальном времени
        if typing:
            t = font.render(text_input + "|", True, current_color)
            screen.blit(t, text_pos)

        # Предпросмотр фигур в реальном времени
        if drawing and start_pos and mode in ['rect', 'circle', 'line']:
            mp = pygame.mouse.get_pos()
            if mode == 'rect':
                pygame.draw.rect(screen, current_color, get_rect(start_pos, mp), size)
            elif mode == 'circle':
                pygame.draw.circle(screen, current_color, start_pos, get_distance(start_pos, mp), size)
            elif mode == 'line':
                pygame.draw.line(screen, current_color, start_pos, mp, size)

        # Отрисовка UI
        pygame.draw.rect(screen, (200, 200, 200), ui_rect)
        for k, r in btns.items():
            if k in colors:
                pygame.draw.rect(screen, colors[k], r)
                # Рамка для индикации выбора цвета
                border = 4 if current_color == colors[k] else 2
                pygame.draw.rect(screen, (0,0,0), r, border)
            else:
                c = (150, 150, 150) if mode == k else (220, 220, 220)
                pygame.draw.rect(screen, c, r)
                pygame.draw.rect(screen, (0, 0, 0), r, 2)
                txt = ui_font.render(k, True, (0, 0, 0))
                screen.blit(txt, (r.x + 5, r.y + 7))
                
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()