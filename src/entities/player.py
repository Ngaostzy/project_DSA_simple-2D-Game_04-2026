import pygame
from src.entities.entity import ENTITY
from src.settings import *

class PLAYER(ENTITY):
    """
    Main Character
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = (255, 150, 50)
        self.speed = 5

    def update(self):
        self.vel_y += GRAVITY

        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY
        
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = - self.speed
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_b]:
            self.vel_x = self.speed
        
        self.x += self.vel_x
        self.y += self.vel_y

    def render(self, screen):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
