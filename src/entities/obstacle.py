import pygame
from src.entities.entity import ENTITY

class OBSTACLE(ENTITY):
    """
    Obstacle for the entities to stand and interact
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = (100, 200, 100)
    
    def render(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)