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

        self.jump_power = -10
        self.is_grounded = False

    def update(self):
        self.vel_y += GRAVITY

        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY
        
        keys = pygame.key.get_pressed()

        self.vel_x = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = - self.speed
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded:
            self.vel_y = self.jump_power
            self.is_grounded = False

        self.x += self.vel_x
        self.y += self.vel_y

    def render(self, screen, camera_x = 0):
        rect = pygame.Rect(self.x - camera_x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
