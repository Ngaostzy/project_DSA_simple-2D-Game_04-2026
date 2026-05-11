import pygame
from src.entities.enemies.enemy_base import ENEMY_BASE
from src.entities.projectile import PROJECTILE

class RANGED_HORIZONTAL(ENEMY_BASE):
    """Represents a ranged hostile entity capable of horizontal projectile emission based on proximity-triggered aggression."""
    def __init__(self, x, y, width, height, hp=3, damage=1):
        """Initializes combat attributes, projectile reservoirs, and temporal cooldown parameters.

        Args:
            x (float): Initial x-coordinate.
            y (float): Initial y-coordinate.
            width (int): Bounding box width.
            height (int): Bounding box height.
            hp (int, optional): Maximum health points. Defaults to 3.
            damage (int, optional): Contact damage payload. Defaults to 1.
        """
        super().__init__(x, y, width, height, hp, damage)
        self.bullets = []
        self.aggro_range = 350
        self.shoot_cooldown = 1500
        self.last_shot_time = 0
        self.image = pygame.image.load("assets/sprites/Weapon.png")

    def shoot(self):
        """Instantiates and propels a projectile along the horizontal axis aligned with the entity's current orientation."""
        vx = 5 if self.facing_right else -5
        vy = 0
        bullet_x = self.x + self.width if self.facing_right else self.x - 10
        bullet_y = self.y + (self.height // 2) - 5
        
        new_bullet = PROJECTILE(bullet_x, bullet_y, vx, vy)
        self.bullets.append(new_bullet)

    def update(self, tiles=None):
        """Advances the kinematic state of the entity and processes spatial updates for all active projectiles.

        Args:
            tiles (list, optional): Environmental grid constraints for projectile collision. Defaults to None.
        """
        super().update()
        if tiles is None: tiles = []
        for bullet in self.bullets: 
            bullet.update(tiles)
        self.bullets = [b for b in self.bullets if not b.is_dead]

    def check_player_interactions(self, player):
        """Evaluates projectile intersections and triggers temporal-based firing sequences within specific spatial boundaries.

        Args:
            player (object): The target entity for collision resolution and proximity detection.
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
        
        dist_x = player.x - self.x 
        dist_y = player.y - self.y

        if abs(dist_x) < self.aggro_range and abs(dist_y) < 150:
            self.facing_right = dist_x > 0
            time_now = pygame.time.get_ticks()
            if time_now - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = time_now
    
    def render(self, screen, camera_x, camera_y):
        """Projects the entity and its active projectiles onto the 2D viewport.

        Args:
            screen (pygame.Surface): The primary display surface.
            camera_x (float): Viewport horizontal translation.
            camera_y (float): Viewport vertical translation.
        """
        super().render(screen, camera_x, camera_y)
        for bullet in self.bullets: 
            bullet.render(screen, camera_x, camera_y)