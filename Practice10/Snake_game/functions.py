import pygame
import random
import psycopg2

# Константы цветов из твоего первого кода
COLORS = {
    "RED": (255, 0, 0),
    "BLUE": (0, 0, 255),
    "GOLD": (255, 215, 0),
    "CYAN": (0, 255, 255),
    "PURPLE": (128, 0, 128),
    "WHITE": (255, 255, 255),
    "DARK_RED": (139, 0, 0)
}

def load_sprites():
    sprites = {}
    try:
        sprites['Grass'] = pygame.image.load("grass.png")
    except:
        s = pygame.Surface((16, 16))
        s.fill((30, 30, 30)); sprites['Grass'] = s # Темный фон, если нет картинки
    return sprites

def spawn_item(snake, width, height, tile_size):
    while True:
        pos = [random.randint(0, (width // tile_size) - 1) * tile_size,
               random.randint(0, (height // tile_size) - 1) * tile_size]
        if pos not in snake:
            return pos

def spawn_food_with_weight(snake, width, height, tile_size):
    pos = spawn_item(snake, width, height, tile_size)
    weight = random.choice([1, 1, 3, 5])
    if weight == 1: color = COLORS["RED"]
    elif weight == 3: color = COLORS["BLUE"]
    else: color = COLORS["GOLD"]
    return {'pos': pos, 'color': color, 'weight': weight}

def spawn_powerup(snake, width, height, tile_size):
    pos = spawn_item(snake, width, height, tile_size)
    ptype = random.choice(["speed", "slow", "shield"])
    color = COLORS["CYAN"] if ptype == "speed" else COLORS["PURPLE"] if ptype == "slow" else COLORS["WHITE"]
    return {'pos': pos, 'type': ptype, 'color': color}

def draw_colored_snake(screen, snake, color):
    for i, seg in enumerate(snake):
        # Голова чуть темнее для отличия
        draw_color = color if i < len(snake) - 1 else (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50))
        pygame.draw.rect(screen, draw_color, (seg[0], seg[1], 16, 16))

# --- БД Функции ---

def get_db():
    return psycopg2.connect("dbname=postgres user=imangaliazamatov password='' host=localhost")

def ensure_db_schema():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS snake_sessions (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50),
                score INTEGER,
                level_reached INTEGER,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("DB Connection Error:", e)

def save_score(username, score, level):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO snake_sessions (username, score, level_reached) VALUES (%s, %s, %s)", 
                    (username, score, level))
        conn.commit()
        conn.close()
    except:
        pass