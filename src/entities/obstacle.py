import pygame
from src.entities.entity import ENTITY

class OBSTACLE(ENTITY):
    """
    Represents a static environmental object within the game world.

    Obstacles serve as physical boundaries, platforms, or floors that dynamic 
    entities (such as the Player or Enemies) can stand on and collide with.
    """

    def __init__(self, x: float, y: float, width: int, height: int):
        """
        Initializes the obstacle with spatial dimensions and visual properties.

        Args:
            x (float): The horizontal coordinate of the top-left corner.
            y (float): The vertical coordinate of the top-left corner.
            width (int): The physical width of the obstacle.
            height (int): The physical height of the obstacle.
        """
        super().__init__(x, y, width, height)
        # Mặc định là một khối màu xanh lá cây
        self.color = (100, 200, 100) 

    def render(self, screen: pygame.Surface, camera_x: float = 0.0) -> None:
        """
        Draws the obstacle onto the display surface relative to the camera.

        Calculates the screen-space position by applying the camera's horizontal 
        offset to the world coordinates, ensuring the obstacle scrolls correctly 
        with the environment.

        Args:
            screen (pygame.Surface): The main display surface to draw on.
            camera_x (float, optional): The horizontal scroll offset of the camera. Defaults to 0.0.
        """
        rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)