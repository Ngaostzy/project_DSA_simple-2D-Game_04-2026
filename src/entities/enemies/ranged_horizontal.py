import pygame
from src.entities.enemies.enemy_base import ENEMY_BASE
from src.entities.projectile import PROJECTILE

class RANGED_HORIZONTAL(ENEMY_BASE):
    def __init__(self, x, y, width, height, hp=3, damage=1):
        super().__init__(x, y, width, height, hp, damage)
        self.bullets = []
        self.aggro_range = 350
        self.shoot_cooldown = 1500
        self.last_shot_time = 0
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((128, 0, 128))

    def shoot(self):
        vx = 5 if self.facing_right else -5
        vy = 0

        bullet_x = self.x + self.width if self.facing_right else self.x - 10
        bullet_y = self.y + (self.height //2) - 5
        new_bullet = PROJECTILE(bullet_x, bullet_y, vx, vy, speed = 5)
        self.bullets.append(new_bullet)

    def update(self):
        super().update()
        for bullet in self.bullets: 
            bullet.update()
        self.bullets = [b for b in self.bullets if not b.is_dead]

    def check_player_interactions(self, player):
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

        if abs(dist_x) < self.aggro_range and abs(dist_y) < 50:
            self.facing_right = dist_x > 0
            time_now = pygame.time.get_ticks()
            if time_now - self.last_shot_time > self.shoot_cooldown:
                self.shoot()
                self.last_shot_time = time_now
    
    def render(self, screen, scroll_x):
        super().render(screen, scroll_x)
        for bullet in self.bullets: bullet.render(screen, scroll_x)

    


