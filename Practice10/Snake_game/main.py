import pygame
from functions import *

pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 304 
TILE_SIZE = 16
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Practice 10")

# Colors and fonts
YELLOW = (255, 223, 0)
font = pygame.font.SysFont("comicsansms", 20)

# Resource loading
SPRITES = load_sprites()

def game_loop():
    clock = pygame.time.Clock()
    fps = 8.0 # Initial speed
    
    # Snake position and movement
    x = (WIDTH // 2 // TILE_SIZE) * TILE_SIZE
    y = (HEIGHT // 2 // TILE_SIZE) * TILE_SIZE
    dx, dy = 0, -TILE_SIZE
    snake = [[x, y + TILE_SIZE], [x, y]]
    
    # Food and progress tracking
    fx1, fy1 = spawn_food(snake, WIDTH, HEIGHT)
    score = 0
    level = 1
    food_to_next_level = 3 # Amount of food required to level up

    run = True
    while run:
        # 1. Background rendering
        for row in range(0, HEIGHT, TILE_SIZE):
            for col in range(0, WIDTH, TILE_SIZE):
                screen.blit(SPRITES['Grass'], (col, row))
        
        # 2. Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -TILE_SIZE
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, TILE_SIZE
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -TILE_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = TILE_SIZE, 0

        # 3. Movement and Wall Collision check
        x += dx
        y += dy
        
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            print("Hit the wall!")
            run = False 

        # 4. Self-collision check
        if [x, y] in snake:
            print("Snake ate itself!")
            run = False

        snake.append([x, y])
        
        # 5. Food consumption and Leveling logic
        if x == fx1 and y == fy1:
            score += 1
            fx1, fy1 = spawn_food(snake, WIDTH, HEIGHT)
            
            # Level up logic
            if score % food_to_next_level == 0:
                level += 1
                fps += 2 # Increase movement speed
        else:
            snake.pop(0)

        # 6. Object rendering
        screen.blit(SPRITES['food'], (fx1, fy1)) 
        draw_snake(screen, snake, SPRITES)
        
        # UI/Statistics display
        score_txt = font.render(f"Score: {score}  Level: {level}", True, YELLOW)
        screen.blit(score_txt, (10, 5))
        
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    game_loop()