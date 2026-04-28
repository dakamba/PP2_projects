import pygame
import random
from config import *

class Food:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.spawn()

    def spawn(self):
        # Генерируем еду так, чтобы она не попала на препятствия
        while True:
            self.pos = (random.randint(0, (WINDOW_WIDTH//CELL_SIZE)-1) * CELL_SIZE,
                        random.randint(0, (WINDOW_HEIGHT//CELL_SIZE)-1) * CELL_SIZE)
            if self.pos not in self.obstacles:
                break
        
        # 20% шанс, что еда будет ядовитой
        self.type = "poison" if random.random() < 0.2 else "normal"
        self.color = DARK_RED if self.type == "poison" else RED
        self.timer = pygame.time.get_ticks() if self.type == "normal" else None

class PowerUp:
    def __init__(self, obstacles):
        self.obstacles = obstacles
        self.type = random.choice(["speed", "slow", "shield"])
        self.spawn_time = pygame.time.get_ticks()
        self.spawn()

    def spawn(self):
        while True:
            self.pos = (random.randint(0, (WINDOW_WIDTH//CELL_SIZE)-1) * CELL_SIZE,
                        random.randint(0, (WINDOW_HEIGHT//CELL_SIZE)-1) * CELL_SIZE)
            if self.pos not in self.obstacles:
                break

class Game:
    def __init__(self, settings, player_id, personal_best):
        self.settings = settings
        self.player_id = player_id
        self.pb = personal_best
        
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = pygame.K_RIGHT
        self.score = 0
        self.level = 1
        self.speed = 10
        
        self.obstacles = []
        self.food = Food(self.obstacles)
        self.powerup = None
        
        self.shield_active = False
        self.powerup_timer = 0
        self.is_powerup_active = False

    def generate_obstacles(self):
        self.obstacles = []
        if self.level >= 3:
            num_blocks = self.level * 2
            for _ in range(num_blocks):
                while True:
                    block = (random.randint(0, (WINDOW_WIDTH//CELL_SIZE)-1) * CELL_SIZE,
                             random.randint(0, (WINDOW_HEIGHT//CELL_SIZE)-1) * CELL_SIZE)
                    # Проверка: не на змейке и не прямо перед головой
                    if block not in self.snake and block != self.snake[0]:
                        self.obstacles.append(block)
                        break

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # Запрет разворота на 180 градусов
                    if (event.key == pygame.K_UP and self.direction != pygame.K_DOWN) or \
                       (event.key == pygame.K_DOWN and self.direction != pygame.K_UP) or \
                       (event.key == pygame.K_LEFT and self.direction != pygame.K_RIGHT) or \
                       (event.key == pygame.K_RIGHT and self.direction != pygame.K_LEFT):
                        self.direction = event.key

        # Движение головы
        head_x, head_y = self.snake[0]
        if self.direction == pygame.K_UP: head_y -= CELL_SIZE
        elif self.direction == pygame.K_DOWN: head_y += CELL_SIZE
        elif self.direction == pygame.K_LEFT: head_x -= CELL_SIZE
        elif self.direction == pygame.K_RIGHT: head_x += CELL_SIZE
        
        new_head = (head_x, head_y)

        # Проверка столкновений (Стены и Препятствия)
        collision = (head_x < 0 or head_x >= WINDOW_WIDTH or 
                     head_y < 0 or head_y >= WINDOW_HEIGHT or 
                     new_head in self.snake or new_head in self.obstacles)

        if collision:
            if self.shield_active:
                self.shield_active = False # Щит спасает один раз
            else:
                return False # Game Over

        self.snake.insert(0, new_head)

        # Поедание еды
        if new_head == self.food.pos:
            if self.food.type == "poison":
                self.snake.pop() # Убираем хвост за текущий ход
                if len(self.snake) > 2:
                    self.snake.pop() # И еще один сегмент (итого -2)
                if len(self.snake) <= 1: return False
            else:
                self.score += 1
                if self.score % 5 == 0: # Повышение уровня каждые 5 очков
                    self.level += 1
                    self.speed += 2
                    self.generate_obstacles()
            self.food = Food(self.obstacles)
        else:
            self.snake.pop()

        # Логика Power-ups (спавн раз в 15 секунд)
        current_time = pygame.time.get_ticks()
        if not self.powerup and not self.is_powerup_active and random.random() < 0.01:
            self.powerup = PowerUp(self.obstacles)

        if self.powerup:
            if new_head == self.powerup.pos:
                self.apply_powerup(self.powerup.type)
                self.powerup = None
            elif current_time - self.powerup.spawn_time > 8000: # Исчезает через 8 сек
                self.powerup = None

        # Сброс эффектов скорости через 5 сек
        if self.is_powerup_active and current_time - self.powerup_timer > 5000:
            self.reset_powerups()

        return True

    def apply_powerup(self, type):
        self.is_powerup_active = True
        self.powerup_timer = pygame.time.get_ticks()
        if type == "speed": self.speed += 7
        elif type == "slow": self.speed = max(5, self.speed - 5)
        elif type == "shield": self.shield_active = True

    def reset_powerups(self):
        self.is_powerup_active = False
        self.speed = 10 + (self.level - 1) * 2 # Возврат к нормальной скорости уровня

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Сетка
        if self.settings.get("grid"):
            for x in range(0, WINDOW_WIDTH, CELL_SIZE):
                pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))

        # Препятствия
        for block in self.obstacles:
            pygame.draw.rect(screen, WHITE, (*block, CELL_SIZE, CELL_SIZE))

        # Змейка
        for i, segment in enumerate(self.snake):
            color = self.settings.get("snake_color", GREEN)
            if i == 0 and self.shield_active: color = BLUE # Голова синяя, если есть щит
            pygame.draw.rect(screen, color, (*segment, CELL_SIZE, CELL_SIZE))

        # Еда и Баффы
        pygame.draw.rect(screen, self.food.color, (*self.food.pos, CELL_SIZE, CELL_SIZE))
        if self.powerup:
            color = YELLOW if self.powerup.type == "speed" else PURPLE
            pygame.draw.rect(screen, color, (*self.powerup.pos, CELL_SIZE, CELL_SIZE))

        # Интерфейс
        font = pygame.font.SysFont("Arial", 20)
        screen.blit(font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {self.level}", True, WHITE), (10, 30))
        screen.blit(font.render(f"PB: {self.pb}", True, YELLOW), (10, 50))