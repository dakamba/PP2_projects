import pygame
import random

# Координаты игровых полос. Используются для того, чтобы машины и монеты 
# появлялись ровно по центру дорожных рядов.
LANES = [220, 340, 460, 580]

class Player(pygame.sprite.Sprite):
    """Класс игрока. Наследуется от Sprite для удобного рендеринга и коллизий."""
    def __init__(self, sprites):
        super().__init__()
        self.sprites = sprites # Список кадров анимации (повороты, движение прямо)
        
        # Начальный кадр (индекс 0 — машина едет прямо)
        self.image = self.sprites[0]
        # Создаем хитбокс (rect) и ставим игрока в нижнюю часть экрана
        self.rect = self.image.get_rect(center=(400, 500))
        self.speed = 8
        self.lives = 5  
        self.sliding_timer = 0 # Таймер для эффекта заноса на масле

    def update(self, **kwargs):
        """Метод обновления состояния игрока в каждом кадре."""
        # ЛОГИКА ЗАНОСА: Если игрок наехал на масло
        if self.sliding_timer > 0:
            # Трясем машину по горизонтали (эффект потери управления)
            self.rect.x += random.randint(-5, 5)
            # Переключаем спрайты случайным образом для эффекта паники
            self.image = self.sprites[random.choice([2, 0, 6])]
            return # Пока идет занос, управление заблокировано

        # ОБЫЧНОЕ УПРАВЛЕНИЕ
        keys = pygame.key.get_pressed()
        # Движение влево с ограничением по краю дороги
        if keys[pygame.K_LEFT] and self.rect.left > 160:
            self.rect.x -= self.speed
            self.image = self.sprites[6] # Визуальный наклон влево
        # Движение вправо
        elif keys[pygame.K_RIGHT] and self.rect.right < 640:
            self.rect.x += self.speed
            self.image = self.sprites[2] # Визуальный наклон вправо
        else:
            self.image = self.sprites[0] # Состояние "прямо", если кнопки не нажаты

class Enemy(pygame.sprite.Sprite):
    """Класс вражеских машин (NPC)."""
    def __init__(self, speed):
        super().__init__()
        try:
            # Загружаем лист со всеми машинами ботов
            sheet = pygame.image.load("assets/Cars/NPC_cars.png").convert_alpha()
            row = random.randint(0, 3) # Выбираем случайный тип машины (ряд в атласе)
            
            # Вырезаем нужную машину (16x16 пикселей в оригинале)
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            self.image.blit(sheet, (0, 0), (0, row * 16, 16, 16))
            # Увеличиваем спрайт под размер игрового экрана
            self.image = pygame.transform.scale(self.image, (80, 80))
        except Exception as e:
            # Заглушка, если файл картинки не найден
            self.image = pygame.Surface((45, 85))
            self.image.fill((200, 50, 50))
            
        # Появляемся на случайной полосе за верхней границей экрана (y = -100)
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        self.speed = speed # Скорость, с которой NPC обгоняет дорогу или едет навстречу

    def update(self, current_speed, **kwargs):
        """NPC движется вниз относительно игрока."""
        # Скорость врага складывается из его собственной и половины скорости дороги
        self.rect.y += self.speed + (current_speed // 2)
        
        # Если машина уехала за нижний край — удаляем её из всех групп
        if self.rect.top > 600:
            self.kill()

class Coin(pygame.sprite.Sprite):
    """Класс бонуса-монеты."""
    def __init__(self, x_pos, value):
        super().__init__()
        self.value = value # Номинал (например, 1 или 5)
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # Рисуем монету программно: Золотая для высокого номинала, серебряная для малого
        color = (255, 215, 0) if value > 2 else (192, 192, 192)
        pygame.draw.circle(self.image, color, (15, 15), 12)
        
        self.rect = self.image.get_rect(center=(x_pos, -50))

    def update(self, current_speed, **kwargs):
        # Монеты "лежат" на дороге, поэтому движутся ровно со скоростью фона
        self.rect.y += current_speed
        if self.rect.top > 600:
            self.kill()

class Prop(pygame.sprite.Sprite):
    """Класс игровых объектов (Масло, Нитро, Барьеры, Щиты)."""
    def __init__(self, sheet_path, prop_type_idx, x_pos):
        super().__init__()
        self.type = prop_type_idx # Запоминаем тип, чтобы знать, какой эффект дать игроку
        try:
            sheet = pygame.image.load(sheet_path).convert_alpha()
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            # Вырезаем нужную иконку из атласа (по горизонтали)
            self.image.blit(sheet, (0, 0), (prop_type_idx * 16, 0, 16, 16))
            self.image = pygame.transform.scale(self.image, (120, 120))
        except:
            self.image = pygame.Surface((120, 120))
            self.image.fill((255, 255, 255))
            
        self.rect = self.image.get_rect(center=(x_pos, -50))

    def update(self, current_speed, **kwargs):
        self.rect.y += current_speed
        if self.rect.top > 600:
            self.kill()

def draw_background(screen, road_img, scroll_y, height):
    """
    ФУНКЦИЯ БЕСКОНЕЧНОГО ФОНА.
    Отрисовывает две копии дороги: одну на текущей позиции, вторую сразу над ней.
    """
    screen.blit(road_img, (0, scroll_y))
    screen.blit(road_img, (0, scroll_y - height))

class FloatingText(pygame.sprite.Sprite):
    """Текст, который плавно взлетает и исчезает (эффект +1 монетка)."""
    def __init__(self, x, y, text, color):
        super().__init__()
        self.font = pygame.font.SysFont("Impact", 30)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.alpha = 255  # Начальная прозрачность (непрозрачный)
        self.timer = 40 

    def update(self, **kwargs):
        self.rect.y -= 2  # Летит вверх
        self.alpha -= 6   # Становится прозрачнее
        if self.alpha <= 0:
            self.kill() # Исчез, удаляем
        else:
            # Применяем прозрачность к картинке текста
            self.image.set_alpha(self.alpha)