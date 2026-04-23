import pygame, sys
from pygame.locals import *
import random, time
import os

# --- INITIALIZATION ---
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
GRAY   = (50, 50, 50)
RED    = (200, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 215, 0)
GREEN  = (34, 139, 34)
BLACK  = (0, 0, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer - Restart & Fixed Rotation")

font_small = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 60)
font_msg = pygame.font.SysFont("Verdana", 30)

def get_sprite_path(filename):
    base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "sprites", filename)

# --- CLASSES ---

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)
        pygame.draw.rect(self.image, BLACK, (0, 0, 50, 80), 2)
        pygame.draw.rect(self.image, YELLOW, (5, 70, 10, 5))
        pygame.draw.rect(self.image, YELLOW, (35, 70, 10, 5))
        
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(65, SCREEN_WIDTH - 65), random.randint(-200, -100))

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1 
            self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self, obstacles):
        super().__init__()
        self.obstacles = obstacles 
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 14)
        pygame.draw.circle(self.image, BLACK, (15, 15), 14, 2)
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        while True:
            new_x = random.randint(65, SCREEN_WIDTH - 65)
            new_y = random.randint(-500, -50)
            self.rect.center = (new_x, new_y)
            # Ensure coins don't spawn directly on top of enemies
            if not pygame.sprite.spritecollideany(self, self.obstacles):
                break

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.spawn()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        try:
            raw_image = pygame.image.load(get_sprite_path("TopDownCar.png")).convert_alpha()
            scaled_image = pygame.transform.scale(raw_image, (90, 50))
            # ROTATION: Set to 90 degrees to orient the car correctly
            self.image = pygame.transform.rotate(scaled_image, 90)
        except:
            # Fallback if image is missing
            self.image = pygame.Surface((45, 80))
            self.image.fill((0, 0, 255))
            
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 45 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH - 45 and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# --- FUNCTIONS ---

def draw_road(surface, offset):
    surface.fill(GREEN)
    pygame.draw.rect(surface, GRAY, (40, 0, SCREEN_WIDTH - 80, SCREEN_HEIGHT))
    pygame.draw.line(surface, WHITE, (40, 0), (40, SCREEN_HEIGHT), 5)
    pygame.draw.line(surface, WHITE, (SCREEN_WIDTH - 40, 0), (SCREEN_WIDTH - 40, SCREEN_HEIGHT), 5)
    
    # Draw animated road markings
    for y in range(-80, SCREEN_HEIGHT + 80, 80):
        pygame.draw.rect(surface, WHITE, (SCREEN_WIDTH // 2 - 5, y + offset, 10, 40))

def reset_game():
    """Resets the game state for a new round"""
    global SCORE, COIN_SCORE, SPEED
    SCORE = 0
    COIN_SCORE = 0
    SPEED = 5
    P1.rect.center = (200, 520)
    E1.spawn()
    C1.spawn()

# --- OBJECT INITIALIZATION ---

P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group(E1)
C1 = Coin(enemies) 
coins = pygame.sprite.Group(C1)
all_sprites = pygame.sprite.Group(P1, E1, C1)

# Increase speed event
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

bg_y = 0
game_over = False

# --- MAIN LOOP ---

while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED and not game_over:
            SPEED += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # If game is over, wait for 'R' key to restart
        if game_over and event.type == KEYDOWN:
            if event.key == K_r:
                game_over = False
                reset_game()

    if not game_over:
        # Movement Logic
        bg_y = (bg_y + SPEED) % 80
        for entity in all_sprites:
            entity.move()

        # Check for coin collection
        if pygame.sprite.spritecollide(P1, coins, False):
            COIN_SCORE += 1
            C1.spawn()

        # Check for collisions with enemies
        if pygame.sprite.spritecollideany(P1, enemies):
            game_over = True

        # Rendering
        draw_road(DISPLAYSURF, bg_y)
        for entity in all_sprites:
            DISPLAYSURF.blit(entity.image, entity.rect)

        # UI / Interface
        scores = font_small.render(f"Dodged: {SCORE}", True, WHITE)
        coin_counter = font_small.render(f"Stars: {COIN_SCORE}", True, YELLOW)
        DISPLAYSURF.blit(scores, (10, 10))
        DISPLAYSURF.blit(coin_counter, (SCREEN_WIDTH - 120, 10))

    else:
        # Game Over Screen
        DISPLAYSURF.fill(RED)
        crash_text = font_large.render("CRASH!", True, WHITE)
        restart_text = font_msg.render("Press R to Restart", True, WHITE)
        
        DISPLAYSURF.blit(crash_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60))
        DISPLAYSURF.blit(restart_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 + 20))

    pygame.display.update()
    FramePerSec.tick(FPS)