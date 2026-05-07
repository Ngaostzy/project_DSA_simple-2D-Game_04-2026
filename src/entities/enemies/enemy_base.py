"""
Module containing the ENEMY_BASE class, the core logic for all enemy types.
"""
from src.entities.entity import ENTITY
from src.settings import *

class ENEMY_BASE(ENTITY):
    def __init__(self, x, y, width, height, hp=3, damage=1):
        super().__init__(x, y, width, height)

        self.hp = hp
        self.damage = damage
        self.is_dead = False
        
        self.facing_right = True

    def check_player_interactions(self, player):
        if self.is_dead:
            return
        
        if (player.x < self.x + self.width and
            player.x + player.width > self.x and
            player.y < self.y + self.height and
            player.y + player.height > self.y):
            
            if not player.is_invincible:
                player.take_damage(self.damage)

                player.vel_y = -5.0 
                if player.x < self.x:
                    player.vel_x = -7.0 
                else: 
                    player.vel_x = 7.0  

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY

    def update(self):
        self.apply_gravity()