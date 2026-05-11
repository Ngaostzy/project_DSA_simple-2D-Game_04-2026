import pygame
from src.entities.enemies.enemy_base import ENEMY_BASE

class PATROL_ENEMY(ENEMY_BASE):
    """Represents a hostile entity with an automated, distance-bounded oscillating patrol routine."""
    def __init__(self, x, y, width, height, patrol_distance=150.0, hp=4, damage=2):
        """Initializes the patrolling entity's kinematic properties, spatial anchors, and visual assets.

        Args:
            x (float): The initial x-coordinate, serving as the central anchor for the patrol route.
            y (float): The initial y-coordinate.
            width (int): Bounding box width.
            height (int): Bounding box height.
            patrol_distance (float, optional): The maximum lateral deviation from the starting anchor. Defaults to 150.0.
            hp (int, optional): Maximum health points. Defaults to 4.
            damage (int, optional): Damage payload delivered upon contact. Defaults to 2.
        """
        super().__init__(x, y, width, height, hp, damage)
        
        self.speed = 1.8 
        self.patrol_distance = patrol_distance
        self.start_x = x
        self.state = 'walk'
        self.scale_factor = 1.7

        try:
            self.sprite_sheet = pygame.image.load("assets/sprites/lava_slime.png")
            self.animation_speeds = {'walk': 0.15} 
            f_size = (64, 64) 
            
            self.animations['walk'] = self.extract_frames(row=0, num_frames=8, frame_size=f_size)
            
            self.image = self.animations['walk'][0]
            
        except FileNotFoundError:
            print("WARNING: Không tìm thấy Slime sprites. Dùng cục gạch đỏ thay thế.")
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))

    def update(self):
        """Processes the entity's frame-by-frame state, strictly enforcing spatial patrol boundaries."""
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