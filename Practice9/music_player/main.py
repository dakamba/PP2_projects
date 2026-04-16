import pygame
from player import MusicPlayer

# Initialize Pygame and the mixer for audio handling
pygame.init()
pygame.mixer.init()

# Window Setup
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pygame Music Player")

# Color Definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)

# Initialize the custom MusicPlayer controller
player = MusicPlayer()

# Font settings for UI text
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

running = True
while running:
    screen.fill(WHITE)
    
    # UI Text Preparation: Fetch current track and playback status
    track_name = player.get_current_track()
    status = "Playing" if player.is_playing() else "Stopped"
    
    # Render text surfaces
    txt_title = font.render(f"Now Playing: {track_name}", True, BLUE)
    txt_status = small_font.render(f"Status: {status}", True, BLACK)
    txt_help = small_font.render("P: Play | S: Stop | N: Next | B: Back | Q: Quit", True, (100, 100, 100))
    
    # Draw text to the screen
    screen.blit(txt_title, (50, 100))
    screen.blit(txt_status, (50, 150))
    screen.blit(txt_help, (50, 300))

    # Event Handling Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Keyboard Input Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.previous()
            elif event.key == pygame.K_q:
                running = False

    # Update the display
    pygame.display.flip()

# Shutdown Pygame
pygame.quit()