import pygame
import random
import os

# Настройка базового пути для поиска ассетов относительно этого файла
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Координаты игровых полос
LANES = [220, 340, 460, 580]

class Player(pygame.sprite.Sprite):
    """Класс игрока с логикой управления и заноса"""
    def __init__(self, sprites):
        super().__init__()
        self.sprites = sprites 
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center=(400, 500))
        self.speed = 8
        self.lives = 5  
        self.sliding_timer = 0 

    def update(self, **kwargs):
        # Логика заноса на масле
        if self.sliding_timer > 0:
            self.rect.x += random.randint(-5, 5)
            self.image = self.sprites[random.choice([2, 0, 6])]
            return 

        # Стандартное управление стрелками
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 160:
            self.rect.x -= self.speed
            self.image = self.sprites[6] 
        elif keys[pygame.K_RIGHT] and self.rect.right < 640:
            self.rect.x += self.speed
            self.image = self.sprites[2] 
        else:
            self.image = self.sprites[0]

class Enemy(pygame.sprite.Sprite):
    """Вражеские машины, вырезаемые из атласа NPC_cars.png"""
    def __init__(self, speed):
        super().__init__()
        try:
            # Используем абсолютный путь к спрайту NPC
            path = os.path.join(BASE_DIR, "assets", "Cars", "NPC_cars.png")
            sheet = pygame.image.load(path).convert_alpha()
            row = random.randint(0, 3) 
            
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
            self.image.blit(sheet, (0, 0), (0, row * 16, 16, 16))
            self.image = pygame.transform.scale(self.image, (80, 80))
        except Exception as e:
            # Заглушка, если файл не найден
            self.image = pygame.Surface((45, 45))
            self.image.fill((200, 50, 50))
            
        self.rect = self.image.get_rect(center=(random.choice(LANES), -100))
        self.speed = speed

    def update(self, current_speed, **kwargs):
        self.rect.y += self.speed + (current_speed // 2)
        if self.rect.top > 600:
            self.kill()

class Coin(pygame.sprite.Sprite):
    """Бонусные монетки (рисуются программно)"""
    def __init__(self, x_pos, value):
        super().__init__()
        self.value = value
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        color = (255, 215, 0) if value > 2 else (192, 192, 192)
        pygame.draw.circle(self.image, color, (15, 15), 12)
        self.rect = self.image.get_rect(center=(x_pos, -50))

    def update(self, current_speed, **kwargs):
        self.rect.y += current_speed
        if self.rect.top > 600:
            self.kill()

class Prop(pygame.sprite.Sprite):
    """Объекты дороги: Масло, Нитро, Барьеры, Щиты"""
    def __init__(self, sheet_path, prop_type_idx, x_pos):
        super().__init__()
        self.type = prop_type_idx 
        try:
            # Корректируем путь к атласу пропсов
            abs_path = os.path.join(BASE_DIR, sheet_path)
            sheet = pygame.image.load(abs_path).convert_alpha()
            
            self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
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
    """Отрисовка зацикленного фона"""
    screen.blit(road_img, (0, scroll_y))
    screen.blit(road_img, (0, scroll_y - height))

class FloatingText(pygame.sprite.Sprite):
    """Всплывающий текст эффектов"""
    def __init__(self, x, y, text, color):
        super().__init__()
        self.font = pygame.font.SysFont("Impact", 30)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.alpha = 255 
        self.timer = 40 

    def update(self, **kwargs):
        self.rect.y -= 2
        self.alpha -= 6 
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)