import pygame
from src.entities.enemies.patrol_enemy import PATROL_ENEMY

class CHASE_ENEMY:
    def __init__(self, x, y, width, height, hp=3, damage=1):
        super().__init__(x, y, width, height, hp, damage)
        self.normal_speed = 1.5
        self.chase_speed = 3.5
        self.vision_range = 250
        self.image.fill((255, 165, 0))

    def check_player_interactions(self, player):
        if self.is_dead: return
        super().check_player_interactions(player)

        dist_x = player.x - self.x
        dist_y = player.y - self.y

        if abs(dist_y) < 50 and abs(dist_x) < self.vision_range:
            is_in_front = (self.facing_right and dist_x > 0) or (not self.facing_right and dist_x < 0)
            if is_in_front:
                self.speed = self.chase_speed
            else:
                self.speed = self.normal_speed
        else:
            self.speed = self.normal_speed
            