import pygame
import sys
from functions import *

pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 400, 320 
TILE_SIZE = 16
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake - Colors Edition")

# Шрифты и системные цвета
font = pygame.font.SysFont("Verdana", 18)

# Загрузка ресурсов и БД
SPRITES = load_sprites()
ensure_db_schema()

def game_loop(username="Player"):
    clock = pygame.time.Clock()
    fps = 8.0 
    
    # Координаты змейки
    x = (WIDTH // 2 // TILE_SIZE) * TILE_SIZE
    y = (HEIGHT // 2 // TILE_SIZE) * TILE_SIZE
    dx, dy = 0, -TILE_SIZE
    snake = [[x, y + TILE_SIZE], [x, y]]
    
    # Объекты (используем логику цветов из первого кода)
    food = spawn_food_with_weight(snake, WIDTH, HEIGHT, TILE_SIZE)
    poison_pos = spawn_item(snake + [food['pos']], WIDTH, HEIGHT, TILE_SIZE)
    powerup = None
    
    score = 0
    level = 1
    food_to_next_level = 3
    shield_active = False

    run = True
    while run:
        # 1. Фон (Трава из спрайтов)
        for row in range(0, HEIGHT, TILE_SIZE):
            for col in range(0, WIDTH, TILE_SIZE):
                screen.blit(SPRITES['Grass'], (col, row))
        
        # 2. Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -TILE_SIZE
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, TILE_SIZE
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -TILE_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = TILE_SIZE, 0

        # 3. Движение и коллизии
        x += dx
        y += dy
        
        collision = False
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or [x, y] in snake:
            collision = True

        if collision:
            if shield_active:
                shield_active = False
                x -= dx; y -= dy # Откат назад
            else:
                save_score(username, score, level)
                run = False 

        snake.append([x, y])
        
        # 4. Поедание еды (с весом: RED=10, BLUE=30, GOLD=50)
        if x == food['pos'][0] and y == food['pos'][1]:
            score += 10 * food['weight']
            food = spawn_food_with_weight(snake, WIDTH, HEIGHT, TILE_SIZE)
            if score >= level * 100:
                level += 1
                fps += 1.5
        # Ядовитая еда (DARK_RED)
        elif x == poison_pos[0] and y == poison_pos[1]:
            if len(snake) > 2:
                snake.pop(0); snake.pop(0)
            poison_pos = spawn_item(snake + [food['pos']], WIDTH, HEIGHT, TILE_SIZE)
        # Бонусы (CYAN, PURPLE, WHITE)
        elif powerup and x == powerup['pos'][0] and y == powerup['pos'][1]:
            if powerup['type'] == 'shield': shield_active = True
            elif powerup['type'] == 'speed': fps += 5
            elif powerup['type'] == 'slow': fps = max(5, fps - 3)
            powerup = None
        else:
            snake.pop(0)

        # 5. Генерация бонуса (редко)
        if not powerup and random.random() < 0.02:
            powerup = spawn_powerup(snake, WIDTH, HEIGHT, TILE_SIZE)

        # 6. Отрисовка объектов
        # Еда (Цвет зависит от веса)
        pygame.draw.rect(screen, food['color'], (*food['pos'], TILE_SIZE, TILE_SIZE))
        
        # Яд (DARK_RED)
        pygame.draw.rect(screen, (139, 0, 0), (*poison_pos, TILE_SIZE, TILE_SIZE))
        
        # Бонус
        if powerup:
            pygame.draw.rect(screen, powerup['color'], (*powerup['pos'], TILE_SIZE, TILE_SIZE))
            
        # Змейка (Если щит — CYAN, иначе GREEN)
        snake_color = (0, 255, 255) if shield_active else (0, 255, 0)
        draw_colored_snake(screen, snake, snake_color)
        
        # Статистика (WHITE)
        score_txt = font.render(f"Score: {score}  Lvl: {level}", True, (255, 255, 255))
        screen.blit(score_txt, (10, 5))
        
        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    game_loop("Azamat")