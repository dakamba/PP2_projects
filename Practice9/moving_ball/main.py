import pygame
from ball import Ball

# Initialize Pygame and set screen dimensions
pygame.init()
W, H = 800, 600
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ball Movement")
clock = pygame.time.Clock()

# Initialize the Ball object at the center of the screen
ball = Ball(W//2, H//2, 25, W, H)

running = True
while running:
    # Clear the screen with a white background
    screen.fill((255, 255, 255))
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Keyboard controls for movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP: 
                ball.move(0, -20)
            elif event.key == pygame.K_DOWN: 
                ball.move(0, 20)
            elif event.key == pygame.K_LEFT: 
                ball.move(-20, 0)
            elif event.key == pygame.K_RIGHT: 
                ball.move(20, 0)

    # Render the ball and update the display
    ball.draw(screen)
    pygame.display.flip()
    
    # Cap the frame rate at 60 FPS
    clock.tick(60)

pygame.quit()