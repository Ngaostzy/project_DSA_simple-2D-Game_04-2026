import pygame

class UI:
    """Manages the Heads-Up Display (HUD) and graphical overlay states for the game."""
    def __init__(self, screen_width, screen_height):
        """Initializes viewport dimensions and typography resources for UI rendering.

        Args:
            screen_width (int): The horizontal resolution of the display window.
            screen_height (int): The vertical resolution of the display window.
        """
        self.width = screen_width
        self.height = screen_height

        self.font_title = pygame.font.Font(None, 100)
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)


    def draw_health_bar(self, screen: pygame.Surface, current_hp, max_hp = 3):
        """Renders discrete hit-point indicators to represent the player's current vitality.

        Args:
            screen (pygame.Surface): The primary display surface to render the HUD on.
            current_hp (int): The player's active health points.
            max_hp (int, optional): The maximum health capacity. Defaults to 3.
        """
        for i in range(max_hp):
            x = 20 + i *40
            y = 20

            if i < current_hp:
                pygame.draw.rect(screen, (220, 20, 60), (x, y, 30, 30), border_radius=5)
            else:
                pygame.draw.rect(screen, (100, 100, 100), (x, y, 30, 30), border_radius=5)
    def draw_game_over(self, screen: pygame.surface):
        """Projects a semi-transparent overlay and state-transition prompts for the end-game sequence.

        Args:
            screen (pygame.Surface): The primary display surface.
        """
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        go_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        go_rect = go_text.get_rect(center=(self.width // 2, self.height //2 -40))
        screen.blit(go_text, go_rect)

        sub_text = self.font_small.render("PRESS [R] to play again or [ESC] to QUIT", True, (255, 255, 255))
        sub_rect = sub_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        screen.blit(sub_text, sub_rect)

class ImageButton:
    """Represents an interactive graphical user interface (GUI) component with sprite scaling."""
    def __init__(self, x, y, image, scale=1.0):
        """Initializes the button's visual representation and spatial bounding box.

        Args:
            x (float): The x-coordinate for the center of the button.
            y (float): The y-coordinate for the center of the button.
            image (pygame.Surface): The base graphical asset for the button.
            scale (float, optional): The uniform scaling multiplier. Defaults to 1.0.
        """
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        """Renders the button sprite onto the designated display surface.

        Args:
            screen (pygame.Surface): The primary rendering surface.
        """
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        """Evaluates pointer-based interaction within the button's collision domain.

        Args:
            event (pygame.event.Event): The input event queued by Pygame.

        Returns:
            bool: True if a left mouse click intersects the bounding box, False otherwise.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False    