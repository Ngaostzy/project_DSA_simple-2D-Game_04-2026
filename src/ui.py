import pygame

class UI:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height

        self.font_title = pygame.font.Font(None, 100)
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)


    def draw_health_bar(self, screen: pygame.Surface, current_hp, max_hp = 3):
        for i in range(max_hp):
            x = 20 + i *40
            y = 20

            if i < current_hp:
                pygame.draw.rect(screen, (220, 20, 60), (x, y, 30, 30), border_radius=5)
            else:
                pygame.draw.rect(screen, (100, 100, 100), (x, y, 30, 30), border_radius=5)
    def draw_game_over(self, screen: pygame.surface):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(150)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))

        go_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        go_rect = go_text.get_rect(center=(self.width // 2, self.height //2 -40))
        screen.blit(go_text, go_rect)

        sub_text = self.font_small.render("Nhấn [R] để Chơi lại hoặc [ESC] để Thoát", True, (255, 255, 255))
        sub_rect = sub_text.get_rect(center=(self.width // 2, self.height // 2 + 40))
        screen.blit(sub_text, sub_rect)

class ImageButton:
    def __init__(self, x, y, image, scale=1.0):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        
        self.rect = self.image.get_rect(center=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False    