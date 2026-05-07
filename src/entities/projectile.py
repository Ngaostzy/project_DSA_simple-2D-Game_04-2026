import pygame
import math


class PROJECTILE:
    def __init__(self, x, y, vx, vy, speed = 5, damage = 1, max_range = 400):
        self.x = x
        self.y = y

        self.width = 10
        self.height = 10

        self.vx = vx
        self.vy = vy

        self.damage = damage
        self.is_dead = False
        self.distance_travel = 0
        self.max_range = max_range
    def update(self):
        self.x += self.vx
        self.y += self.vy

        step_distance = math.sqrt(self.vx**2 + self.vy**2)
        self.distance_travel += step_distance

        if self.distance_travel >= self.max_range:
            self.is_dead = True

    def render(self, screen, scroll_x):
        draw_x = self.x - scroll_x 
        pygame.draw.rect(screen, (255, 215, 0), (draw_x, self.y, self.width, self.height))
    