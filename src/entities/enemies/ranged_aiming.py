import pygame
import math
from src.entities.enemies.enemy_base import ENEMY_BASE
from src.entities.projectile import PROJECTILE

class AIMING_ENEMY(ENEMY_BASE):
    """Represents an aerial hostile entity with sinusoidal hovering mechanics and vector-based projectile targeting."""
    def __init__(self, x, y, width, height, hp=2, damage=1):
        """Initializes combat parameters, floating constraints, and projectile reservoirs.

        Args:
            x (float): Initial x-coordinate.
            y (float): Initial y-coordinate.
            width (int): Bounding box width.
            height (int): Bounding box height.
            hp (int, optional): Maximum health points. Defaults to 2.
            damage (int, optional): Contact damage payload. Defaults to 1.
        """
        super().__init__(x, y, width, height, hp, damage)
        
        self.bullets = [] 
        self.attack_cooldown = 0
        self.attack_range = 400

        self.start_y = y
        self.hover_drop_distance = 100
        
        self.scale_factor = 1.0

        try:
            self.image = pygame.image.load("assets/sprites/Mysterious Bun.png").convert_alpha()
        except FileNotFoundError:
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((128, 0, 128))

    def update(self, tiles=None):
        """Computes sinusoidal vertical displacement and advances the kinematic state of active projectiles.

        Args:
            tiles (list, optional): Environmental grid segments for projectile collision resolution. Defaults to None.
        """
        super().update()

        target_y = self.start_y + self.hover_drop_distance
        if self.start_y > target_y:
            self.vel_y = 0
             
        time_now = pygame.time.get_ticks()
        float_offset = math.sin(time_now / 300.0) * 15

        self.y = target_y + float_offset

        if tiles is None: tiles = []
        for bullet in self.bullets:
            bullet.update(tiles)
        self.bullets = [b for b in self.bullets if not b.is_dead]

    def check_player_interactions(self, player):
        """Resolves projectile-entity intersections and evaluates line-of-sight vector magnitude for attack triggering.

        Args:
            player (object): The target entity for collision and targeting heuristics.
        """
        if self.is_dead: return
        super().check_player_interactions(player)

        for bullet in self.bullets:
            if not bullet.is_dead:
                if (player.x < bullet.x + bullet.width and
                    player.x + player.width > bullet.x and
                    player.y < bullet.y + bullet.height and 
                    player.y + player.height > bullet.y):
                    if not player.is_invincible:
                        player.take_damage(bullet.damage)
                        bullet.is_dead = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        e_cx = self.x + self.width / 2
        e_cy = self.y + self.height / 2
        player_cx = player.x + player.width / 2
        player_cy = player.y + player.height / 2

        dist_x = player_cx - e_cx
        dist_y = player_cy - e_cy

        if abs(dist_x) < self.attack_range and abs(dist_y) < 600:
            self.facing_right = dist_x > 0
            if self.attack_cooldown <= 0:
                self.shoot(dist_x, dist_y)

    def shoot(self, dist_x, dist_y):
        """Normalizes the directional vector towards the target to instantiate and propel a projectile.

        Args:
            dist_x (float): The horizontal scalar distance to the target.
            dist_y (float): The vertical scalar distance to the target.
        """ 
        distance = math.hypot(dist_x, dist_y)
        distance = max(distance, 0.00001)
        
        bullet_speed = 7.0 
        vel_x = (dist_x / distance) * bullet_speed
        vel_y = ((dist_y - 10) / distance) * bullet_speed 

        spawn_x = self.x + self.width / 2
        spawn_y = self.y + self.height / 2
        
        bat = PROJECTILE(spawn_x, spawn_y, vel_x, vel_y)
        self.bullets.append(bat)
        self.attack_cooldown = 60

    def render(self, screen, camera_x, camera_y):
        """Projects the entity and its localized projectile pool onto the viewport.

        Args:
            screen (pygame.Surface): The primary display surface.
            camera_x (float): Viewport horizontal translation.
            camera_y (float): Viewport vertical translation.
        """
        super().render(screen, camera_x, camera_y)
        for bullet in self.bullets: 
            bullet.render(screen, camera_x, camera_y)