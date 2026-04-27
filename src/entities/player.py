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

        self.sprite_sheet = None
        self.animations = {'idle': [], 'run': []}
        self.state = 'idle'
        self.current_frame = 0.0
        self.animation_speeds = {
            'idle': 0.01,
            'run': 0.2
        }

        self.scale_factor = 3
        self.facing_right = True

        try:
            self.sprite_sheet = pygame.image.load("assets/sprites/cat_sheet.png")

            self.animations['idle'] = self.extract_frames(row = 0, num_frames = 6)

            self.animations['run'] = self.extract_frames(row = 6, num_frames = 8)

            self.image = self.animations['idle'][0]
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        except FileNotFoundError:
            print("WARNING: 'cat_sheet.png' not found.")


    def extract_frames(self, row: int, num_frames: int):
        """
        Extracts and scales individual frames from the sprite sheet.

        This method slices out a specific number of frames 
        from a given row on the sprite sheet, scaling them up, and
        storing them in a list for animation sequencing.

        Args:
            row (int): The row index on the sprite sheet containing the animation (0-indexed).
            num_frames (int): The total number of frames to extract from that row.

        Returns:
            list: A list of scaled pygame.Surface objects representing the animation frames.
        """

        frames = []
        frame_width = 32
        frame_height = 32

        for col in range(num_frames):
            surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)

            x_cut = col * frame_width
            y_cut = row * frame_height
            try:
                frame_ref = self.sprite_sheet.subsurface((x_cut, y_cut, frame_width, frame_height))
                frame_surface = frame_ref.copy()

                bounding_rect = frame_surface.get_bounding_rect()
                cropped_surface = frame_surface.subsurface(bounding_rect)

                scaled_surface = pygame.transform.scale_by(cropped_surface, self.scale_factor)
                frames.append(scaled_surface)
            except pygame.error as e:
                print(f"Error extracting frame at row {row}, col {col}: {e}")
                pass

        return frames


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

        if self.sprite_sheet:
            current_anim_list = self.animations[self.state]
            
            speed = self.animation_speeds.get(self.state, 0.15)

            self.current_frame += speed

            if self.current_frame >= len(current_anim_list):
                self.current_frame = 0
            self.image = current_anim_list[int(self.current_frame)]

    def render(self, screen: pygame.surface, camera_x : float = 0) -> None:
        """
        Draws the player's sprite onto the screen surface.
        Calculates the relative screen position based on the camera offset and
        flips the sprite horizontally if the player is facing left.

        Args:
            screen (pygame.Surface): The main display surface.
            camera_x (float): The current horizontal scroll offset of the camera.
        """
        render_x = self.x - camera_x
        image_to_draw = self.image
        if not getattr(self, 'facing_right', True):
            image_to_draw = pygame.transform.flip(self.image, True, False)
        
        screen.blit(image_to_draw, (render_x, self.y))
