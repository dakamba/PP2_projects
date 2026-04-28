import pygame

class Button:
    """
    Универсальный класс для создания кнопок.
    Обрабатывает отрисовку, смену цвета при наведении и клики.
    """
    def __init__(self, text, x, y, width, height, color, hover_color, font_size=25):
        self.text = text
        # Создаем объект Rect для управления границами кнопки
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color             # Основной цвет
        self.hover_color = hover_color # Цвет при наведении мыши
        self.font = pygame.font.SysFont("Impact", font_size)
        
    def draw(self, screen):
        """Отрисовка кнопки на указанном экране."""
        # 1. Проверка наведения: если курсор внутри rect, используем hover_color
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.color
        
        # 2. Рисуем тело кнопки с закругленными углами (border_radius)
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        
        # 3. Рисуем белую рамку толщиной 2 пикселя
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)
        
        # 4. Рендеринг текста и его центрирование внутри кнопки
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        # Создаем rect для текста и совмещаем его центр с центром кнопки
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Проверяет, был ли совершен клик левой кнопкой мыши по этой кнопке."""
        # event.button == 1 — это левая кнопка мыши (LMB)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

def load_car_sprites(filename, scale_factor=5):
    """
    АЛГОРИТМ НАРЕЗКИ СПРАЙТ-ШИТА.
    Разрезает длинную картинку (атлас) на отдельные кадры анимации.
    """
    try:
        # Загружаем всё изображение целиком
        sheet = pygame.image.load(filename).convert_alpha()
        frame_size = 16 # Размер одного квадратного кадра в пикселях
        sprites = []
        
        # Проходим циклом 8 раз (т.к. в атласе машины обычно 8 положений/кадров)
        for i in range(8):
            # Определяем область (rect) текущего кадра на общей картинке
            # i * frame_size сдвигает "окно" захвата вправо на 16 пикселей каждый шаг
            rect = pygame.Rect(i * frame_size, 0, frame_size, frame_size)
            
            # Создаем пустую прозрачную поверхность под один кадр
            frame = pygame.Surface((frame_size, frame_size), pygame.SRCALPHA)
            
            # Копируем (blit) нужный кусок из общего листа на маленькую поверхность
            frame.blit(sheet, (0, 0), rect)
            
            # Увеличиваем кадр (т.к. 16x16 — это слишком мало для экрана 800x600)
            scaled = pygame.transform.scale(frame, (frame_size * scale_factor, frame_size * scale_factor))
            sprites.append(scaled)
            
        return sprites
    except Exception as e:
        print(f"Ошибка в load_car_sprites: {e}")
        # Возвращаем список пустых квадратов, чтобы игра не "крашнулась" при ошибке загрузки
        return [pygame.Surface((80, 80)) for _ in range(8)]