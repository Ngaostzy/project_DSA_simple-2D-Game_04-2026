import pygame
import math
from src.entities.enemies.ranged_horizontal import RANGED_HORIZONTAL
from src.entities.projectile import PROJECTILE

class RANGED_AIMING(RANGED_HORIZONTAL):
    def __init__(self, x, y, width, height, hp=3, damage=1):
        super().__init__(x, y, width, height, hp, damage)
        self.image.fill((255, 0, 0))
        self.bullet_speed = 6

    def shoot(self, target_x, target_y):
        bullet_x = self.x + (self.width //2)
        bullet_y = self.y + (self.height //2)

        angle = math.atan2(target_y - bullet_y, target_x - bullet_x)

        vx = math.cos(angle) * self.bullet_speed
        vy = math.sin(angle) * self.bullet_speed

        new_bullet = PROJECTILE(bullet_x, bullet_y, vx, vy, speed = self.bullet_speed)
        self.bullets.append(new_bullet)

    def check_player_interactions(self, player):
        if self.is_dead: return
        super().check_player_interactions(player)

        dist_x = player.x - self.x
        dist_y = player.y - self.y
        distance_to_player = math.sqrt(dist_x **2 + dist_y ** 2)

        if distance_to_player < 400:
            self.facing_right = dist_x > 0
            time_now = pygame.time.get_ticks()
            if time_now - self.last_shot_time > self.shoot_cooldown:
                self.shoot(player.x + player.width //2, player.y + player.height//2)
                self.last_shot_time = time_now

    

