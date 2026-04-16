import pygame

class Ball:
    def __init__(self, x, y, radius, screen_w, screen_h):
        """Initializes the ball's position, size, and screen boundaries."""
        self.x = x
        self.y = y
        self.radius = radius
        self.screen_w = screen_w
        self.screen_h = screen_h

    def move(self, dx, dy):
        """
        Updates the ball's position while preventing it 
        from moving outside the screen boundaries.
        """
        new_x = self.x + dx
        new_y = self.y + dy

        # Boundary check: ensure the ball's edges stay within the screen width
        if self.radius <= new_x <= self.screen_w - self.radius:
            self.x = new_x
            
        # Boundary check: ensure the ball's edges stay within the screen height
        if self.radius <= new_y <= self.screen_h - self.radius:
            self.y = new_y

    def draw(self, screen):
        """Renders the ball as a red circle on the given surface."""
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)