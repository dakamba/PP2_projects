import pygame
import math

# Class for creating UI buttons
class Button:
    def __init__(self, x, y, width, height, text, action_type, action_value, color=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_type = action_type  # 'tool' or 'color'
        self.action_value = action_value
        self.color = color

    def draw(self, surface, font, is_active):
        # If the button is active, make the background darker for tools
        bg_color = (150, 150, 150) if is_active and self.action_type == 'tool' else self.color
        pygame.draw.rect(surface, bg_color, self.rect)
        
        # Draw border (white if selected, otherwise black)
        border_color = (255, 255, 255) if is_active else (0, 0, 0)
        pygame.draw.rect(surface, border_color, self.rect, 3 if is_active else 1)
        
        # Render text if it exists
        if self.text:
            text_surf = font.render(self.text, True, (0, 0, 0))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Visual Pygame Paint")
    font = pygame.font.SysFont(None, 24)
    
    # Height of the top toolbar
    toolbar_height = 60
    
    # The canvas is smaller than the screen to leave room for the top menu
    canvas = pygame.Surface((screen_width, screen_height - toolbar_height))
    canvas.fill((255, 255, 255))  # Set background to white, like a sheet of paper
    
    clock = pygame.time.Clock()
    
    # Current settings
    current_color = (255, 0, 0)
    current_mode = 'line'
    radius = 5
    
    drawing = False
    start_pos = None
    last_pos = None

    # Define our buttons
    buttons = [
        # Tool buttons
        Button(10, 10, 80, 40, "Line", 'tool', 'line'),
        Button(100, 10, 80, 40, "Rect", 'tool', 'rect'),
        Button(190, 10, 80, 40, "Circle", 'tool', 'circle'),
        Button(280, 10, 80, 40, "Eraser", 'tool', 'eraser'),
        
        # Color buttons (no text, just colored squares)
        Button(400, 10, 40, 40, "", 'color', (255, 0, 0), color=(255, 0, 0)),    # Red
        Button(450, 10, 40, 40, "", 'color', (0, 255, 0), color=(0, 255, 0)),    # Green
        Button(500, 10, 40, 40, "", 'color', (0, 0, 255), color=(0, 0, 255)),    # Blue
        Button(550, 10, 40, 40, "", 'color', (0, 0, 0), color=(0, 0, 0)),        # Black
    ]

    while True:
        # --- 1. EVENT HANDLING ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if the click is within the toolbar area
                    if event.pos[1] < toolbar_height:
                        for btn in buttons:
                            if btn.rect.collidepoint(event.pos):
                                if btn.action_type == 'tool':
                                    current_mode = btn.action_value
                                elif btn.action_type == 'color':
                                    current_color = btn.action_value
                    else:
                        # Clicked below the menu - start drawing
                        drawing = True
                        # Adjust mouse coordinates for the canvas (subtract menu height)
                        canvas_pos = (event.pos[0], event.pos[1] - toolbar_height)
                        start_pos = canvas_pos
                        last_pos = canvas_pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and drawing:
                    canvas_pos = (event.pos[0], event.pos[1] - toolbar_height)
                    if current_mode == 'rect':
                        draw_my_rect(canvas, current_color, start_pos, canvas_pos)
                    elif current_mode == 'circle':
                        draw_my_circle(canvas, current_color, start_pos, canvas_pos)
                drawing = False

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    canvas_pos = (event.pos[0], event.pos[1] - toolbar_height)
                    if current_mode == 'line':
                        pygame.draw.line(canvas, current_color, last_pos, canvas_pos, radius * 2)
                        last_pos = canvas_pos
                    elif current_mode == 'eraser':
                        # Eraser is just drawing with white
                        pygame.draw.line(canvas, (255, 255, 255), last_pos, canvas_pos, radius * 6)
                        last_pos = canvas_pos

        # --- 2. RENDERING ---
        screen.fill((200, 200, 200))  # Toolbar background color (grey)
        
        # Draw the canvas (offset by toolbar_height)
        screen.blit(canvas, (0, toolbar_height)) 
        
        # Draw shape preview directly on the screen over the canvas
        if drawing and start_pos:
            mouse_pos = pygame.mouse.get_pos()
            # Convert canvas coordinates back to screen coordinates for preview
            screen_start = (start_pos[0], start_pos[1] + toolbar_height)
            if current_mode == 'rect':
                draw_my_rect(screen, current_color, screen_start, mouse_pos, width=2)
            elif current_mode == 'circle':
                draw_my_circle(screen, current_color, screen_start, mouse_pos, width=2)

        # Draw menu buttons
        for btn in buttons:
            is_active = (btn.action_value == current_mode) or (btn.action_value == current_color)
            btn.draw(screen, font, is_active)

        pygame.display.flip()
        clock.tick(60)

# --- Helper Functions ---

def draw_my_rect(surface, color, start, end, width=0):
    """Calculates top-left corner and dimensions to draw a rectangle in any direction."""
    x = min(start[0], end[0])
    y = min(start[1], end[1])
    w = abs(start[0] - end[0])
    h = abs(start[1] - end[1])
    if w > 0 and h > 0:
        pygame.draw.rect(surface, color, (x, y, w, h), width)

def draw_my_circle(surface, color, start, end, width=0):
    """Calculates radius using the hypotenuse from start to current mouse position."""
    radius = int(math.hypot(end[0] - start[0], end[1] - start[1]))
    if radius > 0:
        pygame.draw.circle(surface, color, start, radius, width)

if __name__ == "__main__":
    main()