import pygame
from clock import get_hand_position, get_current_time_data

# Initialize Pygame
pygame.init()

# 1. Load the background image first to define window dimensions
temp_image = pygame.image.load("mickeys_clock/images/mickey_hand.png")
WIDTH = temp_image.get_width()
HEIGHT = temp_image.get_height()

# 2. Setup the display window and title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Mouse Clock")

# 3. Optimize image for better performance
bg_image = temp_image.convert() 

# Define clock constants
CENTER = (WIDTH // 2, HEIGHT // 2)
SEC_LEN = int(WIDTH * 0.25)
MIN_LEN = int(WIDTH * 0.15)

clock = pygame.time.Clock()
running = True

# Main Application Loop
while running:
    # Handle user input (Window Close)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fetch updated time angles
    sec_angle, min_angle = get_current_time_data()

    # Render background
    screen.blit(bg_image, (0, 0))

    # Draw the Minute Hand (Black, thicker)
    pygame.draw.line(screen, (0, 0, 0), CENTER, get_hand_position(CENTER, MIN_LEN, min_angle), 6)
    
    # Draw the Second Hand (Red, thinner)
    pygame.draw.line(screen, (255, 0, 0), CENTER, get_hand_position(CENTER, SEC_LEN, sec_angle), 3)
    
    # Draw the center pin
    pygame.draw.circle(screen, (0, 0, 0), CENTER, 15)

    # Refresh display
    pygame.display.flip()
    
    # Maintain 60 FPS for smooth animation
    clock.tick(60)

pygame.quit()