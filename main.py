import sys
import pygame
from src.settings import *
from src.entities.player import PLAYER
from src.core.camera import Camera
from src.core.level import LEVEL
from src.entities.enemies.patrol_enemy import PATROL_ENEMY 
from src.ui import UI
from src.ui import ImageButton
from src.entities.portal import PORTAL
from src.entities.enemies.ranged_aiming import RANGED_AIMING
from src.entities.enemies.ranged_horizontal import RANGED_HORIZONTAL

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nameless Cat - Project")
        self.clock = pygame.time.Clock()
        self.running = True

        
        self.ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera = Camera()
        self.game_state = "START_MENU"
        
        self.reset_game()
        self.game_state = "START_MENU"

        try:
            ui_sheet = pygame.image.load("assets/ui/ui_sheet.png").convert_alpha()
            play_img_cut = ui_sheet.subsurface((240, 128, 57, 25))
            self.btn_play = ImageButton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, play_img_cut, scale=3.0)
        except FileNotFoundError:
            print("Warning: File not found")
            self.btn_play = None


    def reset_game(self):
        self.game_state = 'PLAYING'
        
        self.player = PLAYER(100, 100, TILE_SIZE, TILE_SIZE)
        self.level = LEVEL("assets/maps/map.csv")

        self.portal = PORTAL(300, 500, 64, 64)
        
        self.enemies = [
            PATROL_ENEMY(x=500, y=300, width=32, height=32, patrol_distance=150.0),
            PATROL_ENEMY(x=500, y=100, width=32, height=32),
            RANGED_AIMING(x=500, y=100, width=32, height=32),
            RANGED_HORIZONTAL(x=500, y=100, width=32, height=32)
        ]

    def handle_events(self):
        for event in pygame.event.get():
            if self.game_state == 'START_MENU' and self.btn_play:
                if self.btn_play.is_clicked(event):
                    self.game_state = 'PLAYING'
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_RETURN and self.game_state == 'LEVEL_COMPLETE':
                    self.reset_game()
                
                if event.key == pygame.K_r and self.game_state == 'GAME_OVER':
                    self.reset_game()
            

    def update(self):
        if self.game_state == 'PLAYING':
            self.player.update()
            for enemy in self.enemies:
                enemy.update()
                enemy.check_player_interactions(self.player)
            
            self.player.handle_horizontal_collision(self.level.platforms)
            self.player.handle_vertical_collision(self.level.platforms)
            
            for enemy in self.enemies:
                enemy.handle_horizontal_collision(self.level.platforms)
                enemy.handle_vertical_collision(self.level.platforms)
            
            self.camera.update(self.player)

            if self.player.hp <= 0:
                self.game_state = 'GAME_OVER'
            if self.portal.check_collision(self.player):
                self.game_state = 'LEVEL_COMPLETE'
            

    def render(self):
        if self.game_state == 'START_MENU':
            self.screen.fill((30, 30, 50)) 
            
            if hasattr(self, 'btn_play') and self.btn_play:
                self.btn_play.draw(self.screen)
                
            pygame.display.flip() 
            return
        
        self.screen.fill(BG_COLOR)

        self.level.render(self.screen, self.camera.scroll_x)
        for enemy in self.enemies:
            if not enemy.is_dead:
                enemy.render(self.screen, self.camera.scroll_x)
        
        self.player.render(self.screen, self.camera.scroll_x)

        if self.game_state == 'PLAYING':
            self.ui.draw_health_bar(self.screen, self.player.hp)
            if hasattr(self, 'portal'):
                self.portal.render(self.screen, self.camera.scroll_x)
        elif self.game_state == 'GAME_OVER':
            self.ui.draw_game_over(self.screen)
        elif self.game_state == 'LEVEL_COMPLETE':
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Tạm thời vẽ chay dòng chữ (Bạn có thể bỏ vào ui.py cho đẹp sau)
            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL CLEAR!", True, (0, 255, 0))
            self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50)))
            
            font_small = pygame.font.Font(None, 36)
            text_small = font_small.render("Press [ENTER] for Next Map", True, (255, 255, 255))
            self.screen.blit(text_small, text_small.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50)))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()