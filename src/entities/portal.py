import pygame
import math

class PORTAL:
    def __init__(self, x, y, width=64, height=64):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.base_color = (0, 255, 255)

    def check_collision(self, player):
        if (player.x < self.x + self.width and
            player.x + player.width > self.x and
            player.y < self.y + self.height and 
            player.y + player.height > self.y):
            return True
        return False
    
    def render(self, screen, scroll_x):
        time_now = pygame.time.get_ticks()
        alpha = int(175 + 80 * math.sin(time_now * 0.005))

        self.image.fill((*self.base_color, alpha))

        draw_x = self.x - scroll_x
        screen.blit(self.image, (draw_x, self.y))