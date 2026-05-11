
"""
Module containing the Player class, representing the main controllable character.
"""

import pygame
from src.entities.entity import ENTITY
from src.settings import *

class PLAYER(ENTITY):

    """Represent the main controllable player character.

    The player handles keyboard input, movement physics, animation updates,
    health management, damage invincibility, and rendering.
    """

    def __init__(self, x: float, y: float, width: int, height: int):

        """Initialize the player entity, movement attributes, and animations.

        Args:
            x (float): Initial x-coordinate of the player in world space.
            y (float): Initial y-coordinate of the player in world space.
            width (int): Width of the player's collision box.
            height (int): Height of the player's collision box.
        """

        super().__init__(x, y, width, height)
        self.speed = 5
        self.jump_power = -10
        custom_idle = [(29,0), (29,1), (29,2)]
        
        self.hp = 3
        self.is_invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 60

        self.scale_factor = 2
        try:
            self.sprite_sheet = pygame.image.load("assets/sprites/cat_sheet.png").convert_alpha()

            self.animation_speeds = {'idle': 0.001, 'run': 0.2}

            self.animations['idle'] = self.extract_custom_frames(custom_idle)

            self.animations['run'] = self.extract_frames(row = 6, num_frames = 8)

            self.image = self.animations['idle'][0]
        except FileNotFoundError:
            print("WARNING: 'cat_sheet.png' not found.")

    def update(self) -> None:

        """Update player input, movement physics, invincibility, and animation.

        Applies gravity, limits falling speed, processes keyboard movement,
        handles jumping, and advances the current animation frame.
        """

        if self.is_invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.is_invincible = False

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

        self.update_animations()
    
    def take_damage(self, amount):

        """Apply damage to the player and activate temporary invincibility.

        Args:
            amount (int): Amount of health points to subtract from the player.
        """

        if not self.is_invincible:
            self.hp -= amount
            self.is_invincible = True
            self.invincible_timer = self.invincible_duration 
            
            print(f"Damage taken! HP remain: {self.hp}")
            
            if self.hp <= 0:
                print("💀 GAME OVER!")
    
    def render(self, screen: pygame.Surface, camera_x=0.0, camera_y=0.0):

        """Render the player sprite with camera offset and invincibility effect.

        Args:
            screen (pygame.Surface): Target surface used for rendering.
            camera_x (float): Horizontal camera scroll offset.
            camera_y (float): Vertical camera scroll offset.
        """

        hitbox_x = self.x - camera_x
        hitbox_y = self.y - camera_y

        img_to_draw = self.image

        if self.is_invincible and (self.invincible_timer // 5) % 2 == 0:
            tinted_image = img_to_draw.copy()
            tinted_image.fill(
                (255, 80, 80, 255),
                special_flags=pygame.BLEND_RGBA_MULT
            )
            img_to_draw = tinted_image

        if not self.facing_right:
            img_to_draw = pygame.transform.flip(img_to_draw, True, False)

        sprite_width = img_to_draw.get_width()
        sprite_height = img_to_draw.get_height()

        offset_x = (self.width - sprite_width) // 2

        offset_y = self.height - sprite_height

        draw_x = hitbox_x + offset_x
        draw_y = hitbox_y + offset_y

        screen.blit(img_to_draw, (draw_x, draw_y))

        # pygame.draw.rect(
        #     screen,
        #     (0, 255, 0),
        #     pygame.Rect(hitbox_x, hitbox_y, self.width, self.height),
        #     1
        # )

    # Debug sprite rect
        # pygame.draw.rect(
        #     screen,
        #     (255, 0, 0),
        #     pygame.Rect(draw_x, draw_y, sprite_width, sprite_height),
        #     1   
        # )

