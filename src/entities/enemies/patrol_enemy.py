"""
Module containing the PATROL_ENEMY class.
"""
import pygame
from src.entities.enemies.enemy_base import ENEMY_BASE

class PATROL_ENEMY(ENEMY_BASE):
    def __init__(self, x, y, width, height, patrol_distance=100.0, hp=3, damage=1):
        super().__init__(x, y, width, height, hp, damage)
        
        self.speed = 2.0
        self.patrol_distance = patrol_distance
        self.start_x = x
        self.state = 'walk'
        self.scale_factor = 2

        try:
            self.sprite_sheet = pygame.image.load("assets/sprites/enemy_sheet.png").convert_alpha()
            self.animation_speeds = {'walk': 0.1, 'idle': 0.05}
            self.animations['walk'] = self.extract_frames(row=0, num_frames=4)

            if not self.animations['walk']:
                raise ValueError("ERROR: Animations empty")
            
            self.image = self.animations['walk'][0]
        except FileNotFoundError:
            print("WARNING: 'enemy_sheet.png' not found. Using red placeholder.")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))

    def update(self):
        super().update()

        if self.facing_right:
            self.vel_x = self.speed
            if self.x >= self.start_x + self.patrol_distance:
                self.facing_right = False
        else:
            self.vel_x = -self.speed
            if self.x <= self.start_x - self.patrol_distance:
                self.facing_right = True
        
        self.state = 'walk'
        self.update_animations()