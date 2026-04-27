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

        scale_factor = 0.8

        try:
            raw_image = pygame.image.load("assets/sprite/cat.png").convert_alpha()

            cat_rect = raw_image.get_bounding_rect()
            cropped_image = raw_image.subsurface(cat_rect)

            self.image = pygame.transform.scale_by(cropped_image, scale_factor)

            self.width = self.image.get_width()
            self.height = self.image.get_height()
        except FileNotFoundError:
            print("WARNING: 'cat.png' not found.")


    def update(self) -> None:
        """
        Updates player physics and handles keyboard inputs.
        Args: None
        Return: None
        """

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

    def render(self, screen, camera_x = 0) -> None:
        """
        Draws the player's sprite onto the screen surface.

        Args:
            screen (pygame.Surface): The main display surface.
            camera_x (float): The current horizontal scroll offset of the camera.
        """
        render_x = self.x - camera_x
        screen.blit(self.image, (render_x, self.y))
