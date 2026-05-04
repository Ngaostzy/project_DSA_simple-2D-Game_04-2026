from src.settings import *

class Camera:
    """
    Manages the viewport camera for smooth horizontal scrolling.

    This class tracks and calculates the horizontal offset required to keep 
    a target entity (typically the player) focused on the display screen.
    """
    def __init__(self):
        """
        Initializes the Camera with a default horizontal scroll offset.
        """
        self.scroll_x = 0

    def update(self, target):
        """
        Updates the camera's horizontal offset to follow the target.

        Applies a smooth scrolling algorithm (linear interpolation) by moving
        the camera a fraction of the distance toward the target's center, 
        rather than snapping to it instantly.

        Args:
            target (Entity): The entity to track. Must possess an 'x' 
                             coordinate attribute (e.g., the Player object).
        """
        self.scroll_x += (target.x - self.scroll_x - (SCREEN_WIDTH // 2)) /10