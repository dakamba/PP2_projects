import pygame
import random

# Initialize the underlying Pygame architecture and multimedia subsystems
pygame.init()

# --- Structural & Environmental Constants ---
WIDTH, HEIGHT = 800, 608  # Spatial bounds of the display surface
TILE_SIZE = 16            # Grid resolution (cell dimension in pixels)
FPS = 9.0                 # Temporal resolution (frames per second)

# --- Color Vectors (RGB color space) ---
YELLOW = (255, 223, 0)
GREEN_BG = (124, 252, 0)

# --- Display & UI Instantiation ---
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Flip - Toroidal Spatial Edition")
clock = pygame.time.Clock()  # Temporal controller for standardizing the main loop
score_font = pygame.font.SysFont("comicsansms", 25)

def load_sprites():
    """
    Ingests the primary sprite sheet and partitions it into discrete sub-surfaces.
    Utilizes alpha compositing for transparent backgrounds.
    """
    try:
        # Load the graphical matrix into memory
        sheet = pygame.image.load("SnakeFlip.png").convert_alpha()
    except FileNotFoundError:
        print("Fatal Exception: Asset 'SnakeFlip.png' could not be located.")
        pygame.quit()
        quit()

    s = TILE_SIZE # Dimensional scalar (16px)
    
    def get_at(col, row):
        """
        Extracts a localized matrix (16x16 pixels) from the primary sprite sheet
        based on Cartesian column and row indices.
        """
        surf = pygame.Surface((s, s), pygame.SRCALPHA)
        # blit arguments: source, destination coordinates, cutting boundary (x, y, width, height)
        surf.blit(sheet, (0, 0), (col * s, row * s, s, s))
        return surf

    # Return a mapped dictionary of graphical assets for constant-time (O(1)) retrieval
    return {
        # Terminal Node (Head) Orientations
        'head_U': get_at(0, 0), 'head_R': get_at(1, 0), 'head_D': get_at(2, 0), 'head_L': get_at(3, 0),
        # Initial Node (Tail) Orientations
        'tail_U': get_at(0, 1), 'tail_R': get_at(1, 1), 'tail_D': get_at(2, 1), 'tail_L': get_at(3, 1),
        # Intermediary Node Transformations (Corners/Bends)
        'tr_UL': get_at(2, 2), 'tr_UR': get_at(1, 2), 'tr_DL': get_at(0, 2), 'tr_DR': get_at(3, 2),
        # Linear Intermediary Nodes and Environmental Entities
        'body_V': get_at(0, 3), 'body_H': get_at(1, 3), 'food': get_at(2, 3), 
        'Grass': get_at(3, 3)
    }

# Instantiate the graphical asset dictionary sequentially at runtime
SPRITES = load_sprites()

def get_rel_dir(curr, other):
    """
    Computes the relative spatial orientation vector between two coordinate loci.
    Crucially, this accounts for toroidal space bounds (screen wrapping) to ensure
    continuous graphical alignment when the entity spans across opposite spatial boundaries.
    """
    dx = curr[0] - other[0]
    dy = curr[1] - other[1]

    # Toroidal correction: If the delta exceeds a single grid cell distance, 
    # a boundary transposition has occurred. The vector is inverted to maintain logical continuity.
    if dx > TILE_SIZE: dx = -TILE_SIZE
    elif dx < -TILE_SIZE: dx = TILE_SIZE
    
    if dy > TILE_SIZE: dy = -TILE_SIZE
    elif dy < -TILE_SIZE: dy = TILE_SIZE
    
    return dx, dy

def draw_snake(snake_list):
    """
    Iterates through the topological queue of the primary entity (the snake).
    Evaluates the adjacency of neighboring nodes to map the appropriate graphical texture.
    """
    for i, (x, y) in enumerate(snake_list):
        pos = (x, y)
        
        # --- 1. Terminal Node Computation (Head) ---
        if i == len(snake_list) - 1:
            # Determine trajectory vector relative to the adjacent anatomical node
            prev = snake_list[i-1] if len(snake_list) > 1 else (x, y + TILE_SIZE)
            dx, dy = get_rel_dir((x, y), prev)
            
            if dx > 0: img = SPRITES['head_R']
            elif dx < 0: img = SPRITES['head_L']
            elif dy > 0: img = SPRITES['head_D']
            else: img = SPRITES['head_U']
            
        # --- 2. Initial Node Computation (Tail) ---
        elif i == 0:
            nxt = snake_list[i+1]
            dx, dy = get_rel_dir(nxt, (x, y)) 
            
            if dx > 0: img = SPRITES['tail_R']
            elif dx < 0: img = SPRITES['tail_L']
            elif dy > 0: img = SPRITES['tail_D']
            else: img = SPRITES['tail_U']
            
        # --- 3. Intermediary Node Computation (Body and Transformations) ---
        else:
            p, n = snake_list[i-1], snake_list[i+1]
            # Derive orientation vectors relative to both adjacent nodes
            dx_p, dy_p = get_rel_dir(p, (x, y))
            dx_n, dy_n = get_rel_dir(n, (x, y))

            # Linear alignment evaluation
            if dx_p == -dx_n and dy_p == -dy_n:
                if dx_p != 0: img = SPRITES['body_H'] # Horizontal axis
                else: img = SPRITES['body_V']         # Vertical axis
            # Non-linear alignment (corner computation)
            else:
                if (dx_p == -TILE_SIZE and dy_n == -TILE_SIZE) or (dx_n == -TILE_SIZE and dy_p == -TILE_SIZE):
                    img = SPRITES['tr_DR']
                elif (dx_p == TILE_SIZE and dy_n == -TILE_SIZE) or (dx_n == TILE_SIZE and dy_p == -TILE_SIZE):
                    img = SPRITES['tr_DL']
                elif (dx_p == -TILE_SIZE and dy_n == TILE_SIZE) or (dx_n == -TILE_SIZE and dy_p == TILE_SIZE):
                    img = SPRITES['tr_UL']
                else:
                    img = SPRITES['tr_UR']
        
        # Dispatch the computed asset to the display buffer
        screen.blit(img, pos)

def spawn_food(snake):
    """
    Procedurally generates spatial coordinates for consumable entities.
    Utilizes rejection sampling to prevent spatial superposition with the primary entity.
    """
    while True:
        fx = random.randrange(0, WIDTH, TILE_SIZE)
        fy = random.randrange(0, HEIGHT, TILE_SIZE)
        
        # Verify that the generated locus is mutually exclusive from the snake's occupied coordinate set
        if [fx, fy] not in snake:
            return [fx, fy]

def game_loop():
    """
    The primary execution and event-handling loop.
    Manages state mutation, collision detection algorithms, and rendering dispatch.
    """
    global FPS
    
    # Initialize origin point utilizing integer division for grid alignment
    x = (WIDTH // 2 // TILE_SIZE) * TILE_SIZE
    y = (HEIGHT // 2 // TILE_SIZE) * TILE_SIZE
    
    # Initial trajectory vector (Negative Y implies upward translation)
    dx, dy = 0, -TILE_SIZE
    
    # Instantiation of the primary entity's spatial queue [Initial Node, Terminal Node]
    snake = [[x, y + TILE_SIZE], [x, y]] 
    
    # Procedural generation of initial consumable entities
    fx1, fy1 = spawn_food(snake)
    fx2, fy2 = spawn_food(snake)

    run = True
    while run:
        # 1. Environmental Rendering (Background Matrix)
        for row in range(0, HEIGHT, TILE_SIZE):
            for col in range(0, WIDTH, TILE_SIZE):
                screen.blit(SPRITES['Grass'], (col, row))
        
        # 2. Asynchronous Input Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Orthogonal constraint logic: prohibits 180-degree vector inversions in a single temporal cycle
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -TILE_SIZE
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, TILE_SIZE
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -TILE_SIZE, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = TILE_SIZE, 0
                elif event.key == pygame.K_SPACE:
                    FPS *= 3 # Temporal resolution modulation (Acceleration)
    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    FPS /= 3 # Temporal resolution modulation (Deceleration)

        # 3. Spatial Translation Module
        # Modulo operators (%) implement a toroidal spatial manifold (borderless bounds)
        x = (x + dx) % WIDTH
        y = (y + dy) % HEIGHT
        
        # 4. Self-Intersection Evaluation (Collision Detection)
        if [x, y] in snake:
            run = False # Termination sequence initiated upon logical overlap

        # Mutate the topological queue by appending the new spatial terminus
        snake.append([x, y])
        
        # 5. Consumption Logic (Growth and Resource Re-allocation)
        if x == fx1 and y == fy1:
            # Re-allocate locus of consumable entity 1; bypass deletion of initial node to permit growth
            fx1, fy1 = spawn_food(snake)
        elif x == fx2 and y == fy2:
            # Re-allocate locus of consumable entity 2
            fx2, fy2 = spawn_food(snake)
        else:
            # Standard translation state: dequeue the earliest node to maintain static structural length
            snake.pop(0)

        # 6. Final Buffer Dispatch
        screen.blit(SPRITES['food'], (fx1, fy1)) 
        screen.blit(SPRITES['food'], (fx2, fy2)) 
        draw_snake(snake)                        
        
        # Quantitative Metric Rendering (Score)
        score_txt = score_font.render(f"Score: {len(snake)-2}", True, YELLOW)
        screen.blit(score_txt, (10, 10))
        
        # Push the localized display buffer to the primary screen and throttle loop iteration
        pygame.display.flip()
        clock.tick(FPS)

    # Teardown the subsystem gracefully
    pygame.quit()

# Entry point of execution
if __name__ == "__main__":
    game_loop()