"""
Module containing the ENEMY_BASE class, the core logic for all enemy types.
"""
from src.entities.entity import ENTITY
from src.settings import *
import pygame

class ENEMY_BASE(ENTITY):
    """Abstract base class for hostile entities, managing kinematics, spatial awareness, and combat resolution."""
    def __init__(self, x, y, width, height, hp=3, damage=1):
        """Initializes foundational attributes for the enemy entity.

        Args:
            x (float): The initial x-coordinate of the entity.
            y (float): The initial y-coordinate of the entity.
            width (int): Bounding box width.
            height (int): Bounding box height.
            hp (int, optional): Maximum health points. Defaults to 3.
            damage (int, optional): Damage payload delivered upon contact. Defaults to 1.
        """
        super().__init__(x, y, width, height)

        self.hp = hp
        self.damage = damage
        self.is_dead = False
        
        self.facing_right = True

    def check_player_interactions(self, player):
        """Evaluates AABB intersection with the player, applying damage and kinetic knockback.

        Args:
            player (object): The player entity instance to check against.
        """
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
    
    def handle_horizontal_collision(self, spatial_platforms):
        """Resolves lateral displacement against environmental constraints via raycasting and edge detection.

        Args:
            spatial_platforms (list/dict): A collection of platform bounds for spatial queries.
        """

        nearby = self.get_nearby_platforms(spatial_platforms)

        if self.is_grounded and self.vel_x != 0:
            sensor_x = self.x + self.width + 5 if self.vel_x >0 else self.x - 5
            sensor_rect = pygame.Rect(sensor_x, self.y + self.height, 2, 100)

            has_floor_ahead = False
            for plat in nearby:
                if plat.colliderect(sensor_rect):
                    has_floor_ahead = True
                    break
            if not has_floor_ahead:
                self.facing_right = not self.facing_right
                speed_val = getattr(self, 'speed', 1.5)
                self.vel_x = speed_val if self.facing_right else -speed_val

                if hasattr(self, 'ignore_player_timer'):
                    self.ignore_player_timer = 60
            
        self.x += self.vel_x
        if self.vel_x == 0:
            return
        
        hit_wall = False
        hit_plat = None

        for plat in nearby:
            if self.y + self.height > plat.y and self.y < plat.y + plat.height:
                if self.x + self.width > plat.x and self.x < plat.x + plat.width:
                    if self.vel_x > 0:
                        self.x = plat.x - self.width
                    elif self.vel_x < 0:
                        self.x = plat.x + plat.width

                    self.vel_x = 0
                    hit_wall = True
                    hit_plat = plat
                    break

        if hit_wall and self.is_grounded:
            j_strenth = getattr(self, 'jump_strength', -7.5)
            obstacle_height = (self.y + self.height) - hit_plat.y

            if 0 < obstacle_height <=35:
                col = hit_plat.x // 32
                row = (hit_plat.y - 32) //2

                is_blocked_ahead = (col, row) in spatial_platforms
    
                if not is_blocked_ahead:
                    self.vel_y = j_strenth
                    self.is_grounded = False
                    speed_val = getattr(self, 'speed', 1.5)
                    self.vel_x = speed_val if self.facing_right else -speed_val
                    return
                
            self.facing_right = not self.facing_right
            if hasattr(self, 'ignore_player_timer'):
                self.ignore_player_timer = 60


    def apply_gravity(self):
        """Applies continuous downward acceleration bounded by terminal velocity."""
        self.vel_y += GRAVITY
        if self.vel_y > TERMINAL_VELOCITY:
            self.vel_y = TERMINAL_VELOCITY

    def update(self):
        """Advances the kinematic state of the entity per logical frame."""
        self.apply_gravity()