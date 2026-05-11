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
from src.entities.enemies.ranged_aiming import AIMING_ENEMY
from src.entities.enemies.ranged_horizontal import RANGED_HORIZONTAL
from src.entities.enemies.chase_enemy import CHASE_ENEMY
from src.entities.spikes import SPIKE


class Game:
    """Orchestrates the primary application loop, state machine transitions, and subsystem integrations."""
    def __init__(self):
        """Initializes the SDL display surface, core managers, and pre-loads initial GUI assets."""
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Nameless Cat - Project")

        self.clock = pygame.time.Clock()
        self.running = True

        self.ui = UI(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.game_state = "START_MENU"

        self.level = None
        self.player = None
        self.portal = None
        self.enemies = []
        self.spikes = []

        try:
            ui_sheet = pygame.image.load("assets/ui/ui_sheet.png").convert_alpha()
            play_img_cut = ui_sheet.subsurface((240, 128, 57, 25))
            self.btn_play = ImageButton(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                play_img_cut,
                scale=3.0
            )
        except FileNotFoundError:
            print("[MAIN] ⚠️ Không tìm thấy assets/ui/ui_sheet.png")
            self.btn_play = None

    def reset_game(self):
        """Reconstructs the level topology and populates entities based on spatial map data."""
        self.game_state = "PLAYING"

        self.level = LEVEL("assets/maps/map_3.0.ldtk")

        px, py = self.level.spawn_points["Player"]
        self.player = PLAYER(px, py, 32, 32)

        pox, poy = self.level.spawn_points["Portal"]
        self.portal = PORTAL(pox, poy, TILE_SIZE * 2, TILE_SIZE * 2)

        self.enemies = []
        self.spikes = []

        for entity_type, ex, ey in self.level.spawn_points["Enemies"]:
            if entity_type == "Enemy_Patrol":
                self.enemies.append(PATROL_ENEMY(ex, ey, 32, 32))

            elif entity_type == "Aiming_enemy":
                self.enemies.append(AIMING_ENEMY(ex, ey, 32, 32))

            elif entity_type == "Enemy_chase":
                self.enemies.append(CHASE_ENEMY(ex, ey, 32, 32))

            elif entity_type == "Ranged_horizontal_enemy":
                self.enemies.append(RANGED_HORIZONTAL(ex, ey, 32, 32))

            elif entity_type == "Spikes_Up":
                self.spikes.append(SPIKE(ex, ey, 32, 57, "up"))

            elif entity_type == "Spikes_Down":
                self.spikes.append(SPIKE(ex, ey, 32, 57, "down"))

            else:
                print("[MAIN] Entity chưa xử lý:", entity_type)

    def handle_events(self):
        """Processes the asynchronous input queue for window management and state-transition keystrokes."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.game_state == "START_MENU" and self.btn_play:
                if self.btn_play.is_clicked(event):
                    self.reset_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.key == pygame.K_RETURN and self.game_state == "LEVEL_COMPLETE":
                    self.reset_game()

                if event.key == pygame.K_r and self.game_state == "GAME_OVER":
                    self.reset_game()

    def update(self):
        """Advances the kinematic logic for all active entities and evaluates global state triggers."""
        if self.game_state != "PLAYING":
            return

        self.player.update()

        for enemy in self.enemies:
            if enemy.is_dead:
                continue

            if hasattr(enemy, "bullets"):
                enemy.update(self.level.spatial_platforms)
            else:
                enemy.update()

            enemy.check_player_interactions(self.player)
            enemy.handle_horizontal_collision(self.level.spatial_platforms)
            enemy.handle_vertical_collision(self.level.spatial_platforms)

        self.player.handle_horizontal_collision(self.level.spatial_platforms)
        self.player.handle_vertical_collision(self.level.spatial_platforms)

        for spike in self.spikes:
            spike.check_collision(self.player)

        self.camera.update(
            self.player,
            self.level.width,
            self.level.height
        )

        if self.player.hp <= 0:
            self.game_state = "GAME_OVER"

        if self.portal and self.portal.check_collision(self.player):
            self.game_state = "LEVEL_COMPLETE"

    def render(self):
        """Projects the temporal state of the environment, entities, and UI overlays onto the 2D display surface."""
        if self.game_state == "START_MENU":
            self.screen.fill((30, 30, 50))

            if self.btn_play:
                self.btn_play.draw(self.screen)
            else:
                font = pygame.font.Font(None, 48)
                text = font.render("Press ENTER to Play", True, (255, 255, 255))
                rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(text, rect)

            pygame.display.flip()
            return

        self.screen.fill(BG_COLOR)

        if self.level:
            self.level.render(
                self.screen,
                self.camera.scroll_x,
                self.camera.scroll_y
            )

        for spike in self.spikes:
            spike.render(
                self.screen,
                self.camera.scroll_x,
                self.camera.scroll_y
            )

        for enemy in self.enemies:
            if not enemy.is_dead:
                enemy.render(
                    self.screen,
                    self.camera.scroll_x,
                    self.camera.scroll_y
                )

        if self.player:
            self.player.render(
                self.screen,
                self.camera.scroll_x,
                self.camera.scroll_y
            )

        if self.portal:
            self.portal.render(
                self.screen,
                self.camera.scroll_x,
                self.camera.scroll_y
            )

        if self.game_state == "PLAYING":
            self.ui.draw_health_bar(self.screen, self.player.hp)

        elif self.game_state == "GAME_OVER":
            self.ui.draw_game_over(self.screen)

        elif self.game_state == "LEVEL_COMPLETE":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))

            font = pygame.font.Font(None, 74)
            text = font.render("LEVEL CLEAR!", True, (0, 255, 0))
            self.screen.blit(
                text,
                text.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                )
            )

            font_small = pygame.font.Font(None, 36)
            text_small = font_small.render(
                "Press [ENTER] for Next Map",
                True,
                (255, 255, 255)
            )
            self.screen.blit(
                text_small,
                text_small.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
                )
            )

        pygame.display.flip()

    def run(self):
        """Executes the deterministic game loop, synchronizing updates and rendering with the target frame rate."""
        while self.running:
            self.handle_events()

            keys = pygame.key.get_pressed()
            if self.game_state == "START_MENU" and not self.btn_play:
                if keys[pygame.K_RETURN]:
                    self.reset_game()

            self.update()
            self.render()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()