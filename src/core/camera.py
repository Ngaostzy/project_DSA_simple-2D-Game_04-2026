from src.settings import *

class Camera:
    def __init__(self):
        self.scroll_x = 0

    def update(self, target):
        self.scroll_x += (target.x - self.scroll_x - (SCREEN_WIDTH // 2)) /10