import pygame
import math

class PORTAL:
    """Represents a portal entity for spatial transitions within the game environment."""
    def __init__(self, x, y, width=64, height=64):
        """Initializes the portal's spatial dimensions and visual properties.

        Args:
            x (float): The x-coordinate of the portal's top-left corner.
            y (float): The y-coordinate of the portal's top-left corner.
            width (int, optional): The bounding box width in pixels. Defaults to 64.
            height (int, optional): The bounding box height in pixels. Defaults to 64.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.base_color = (0, 255, 255)

    def check_collision(self, player):
        """Evaluates Axis-Aligned Bounding Box (AABB) collision between the portal and the player.

        Args:
            player (object): The player entity instance. Must possess 'x', 'y', 'width', and 'height' attributes.

        Returns:
            bool: True if bounding boxes intersect, False otherwise.
        """
        if (player.x < self.x + self.width and
            player.x + player.width > self.x and
            player.y < self.y + self.height and 
            player.y + player.height > self.y):
            return True
        return False
    
    def render(self, screen, scroll_x, scroll_y):
        """Renders the portal onto the display surface with a time-based oscillating alpha effect.

        Args:
            screen (pygame.Surface): The primary display surface to render the portal on.
            scroll_x (float): The current horizontal camera offset.
            scroll_y (float): The current vertical camera offset.
        """
        time_now = pygame.time.get_ticks()
        alpha = int(175 + 80 * math.sin(time_now * 0.005))

        self.image.fill((*self.base_color, alpha))

        draw_x = self.x - scroll_x
        draw_y = self.y - scroll_y
        screen.blit(self.image, (draw_x, draw_y))