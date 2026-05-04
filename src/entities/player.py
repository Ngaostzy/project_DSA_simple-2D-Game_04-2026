"""
Module containing the Player class, representing the main controllable character.
"""
import pygame
from src.entities.entity import ENTITY
from src.settings import *

class PLAYER(ENTITY):
    """
    The main player character, inheriting from Entity.

    Attributes:
        image (pygame.Surface): The graphical representation of the player.
        jump_power (float): The upward velocity applied when jumping.
        is_grounded (bool): State flag indicating if the player is resting on a surface.
    """
    def __init__(self, x: float, y: float, width: int, height: int):
        """
        Initializes the player entity and loads its sprite.

        Args:
            x (float): Initial X coordinate in world space.
            y (float): Initial Y coordinate in world space.
            width (int): Width of the character's bounding box.
            height (int): Height of the character's bounding box.
        """
        super().__init__(x, y, width, height)
        self.speed = 5
        self.jump_power = -10
        self.is_grounded = False
        custom_idle = [(29,0), (29,1), (29,2)]

        self.scale_factor = 3
        try:
            self.sprite_sheet = pygame.image.load("assets/sprites/cat_sheet.png").convert_alpha()

            self.animation_speeds = {'idle': 0.01, 'run': 0.2}

            self.animations['idle'] = self.extract_custom_frames(custom_idle)

            self.animations['run'] = self.extract_frames(row = 6, num_frames = 8)

            self.image = self.animations['idle'][0]
        except FileNotFoundError:
            print("WARNING: 'cat_sheet.png' not found.")

    def update(self) -> None:
        """
        Updates player physics and handles keyboard inputs
        and advances the animation.
        Args: None
        Return: None
        """

        self.vel_y += GRAVITY

        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY
        
        keys = pygame.key.get_pressed()
        self.vel_x = 0

        self.state = 'idle'

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = - self.speed
            self.state = 'run'
            self.facing_right = False
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            self.state = 'run'
            self.facing_right = True
        
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded:
            self.vel_y = self.jump_power
            self.is_grounded = False

        self.x += self.vel_x
        self.y += self.vel_y

        self.update_animations()