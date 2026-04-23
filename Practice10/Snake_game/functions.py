import pygame
import random
import os

# Grid constants
TILE_SIZE = 16

def load_sprites():
    """
    Loads the sprite sheet and slices it into individual parts.
    Uses os.path to ensure cross-platform path compatibility.
    """
    base_path = os.path.dirname(__file__)
    image_path = os.path.join(base_path, "snake_image\SnakeFlip.png")
    
    try:
        sheet = pygame.image.load(image_path).convert_alpha()
    except FileNotFoundError:
        print(f"Error: File {image_path} not found!")
        pygame.quit()
        exit()

    s = TILE_SIZE 
    
    def get_at(col, row):
        """Helper to extract a single tile from the sprite sheet."""
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        surf.blit(sheet, (0, 0), (col * s, row * s, s, s))
        return surf

    return {
        'head_U': get_at(0, 0), 'head_R': get_at(1, 0), 'head_D': get_at(2, 0), 'head_L': get_at(3, 0),
        'tail_U': get_at(0, 1), 'tail_R': get_at(1, 1), 'tail_D': get_at(2, 1), 'tail_L': get_at(3, 1),
        'tr_UL': get_at(2, 2), 'tr_UR': get_at(1, 2), 'tr_DL': get_at(0, 2), 'tr_DR': get_at(3, 2),
        'body_V': get_at(0, 3), 'body_H': get_at(1, 3), 'food': get_at(2, 3), 
        'Grass': get_at(3, 3)
    }

def get_rel_dir(curr, other):
    """Calculates the relative direction vector between two segments."""
    dx = curr[0] - other[0]
    dy = curr[1] - other[1]
    return dx, dy

def draw_snake(screen, snake_list, sprites):
    """Renders the snake by selecting the appropriate sprite for each segment."""
    for i, (x, y) in enumerate(snake_list):
        if i == len(snake_list) - 1: # Head segment
            prev = snake_list[i-1] if len(snake_list) > 1 else (x, y + TILE_SIZE)
            dx, dy = get_rel_dir((x, y), prev)
            if dx > 0: img = sprites['head_R']
            elif dx < 0: img = sprites['head_L']
            elif dy > 0: img = sprites['head_D']
            else: img = sprites['head_U']
            
        elif i == 0: # Tail segment
            nxt = snake_list[i+1]
            dx, dy = get_rel_dir(nxt, (x, y)) 
            if dx > 0: img = sprites['tail_R']
            elif dx < 0: img = sprites['tail_L']
            elif dy > 0: img = sprites['tail_D']
            else: img = sprites['tail_U']
            
        else: # Body segments and corners
            p, n = snake_list[i-1], snake_list[i+1]
            dx_p, dy_p = get_rel_dir(p, (x, y))
            dx_n, dy_n = get_rel_dir(n, (x, y))

            # Check if it's a straight body part
            if dx_p == -dx_n and dy_p == -dy_n:
                img = sprites['body_H'] if dx_p != 0 else sprites['body_V']
            else:
                # Handle corner (turn) sprites
                if (dx_p == -TILE_SIZE and dy_n == -TILE_SIZE) or (dx_n == -TILE_SIZE and dy_p == -TILE_SIZE):
                    img = sprites['tr_DR']
                elif (dx_p == TILE_SIZE and dy_n == -TILE_SIZE) or (dx_n == TILE_SIZE and dy_p == -TILE_SIZE):
                    img = sprites['tr_DL']
                elif (dx_p == -TILE_SIZE and dy_n == TILE_SIZE) or (dx_n == -TILE_SIZE and dy_p == TILE_SIZE):
                    img = sprites['tr_UL']
                else:
                    img = sprites['tr_UR']
        
        screen.blit(img, (x, y))

def spawn_food(snake, width, height):
    """Generates food coordinates ensuring they don't overlap with the snake body."""
    while True:
        fx = random.randrange(0, width, TILE_SIZE)
        fy = random.randrange(0, height, TILE_SIZE)
        if [fx, fy] not in snake:
            return [fx, fy]