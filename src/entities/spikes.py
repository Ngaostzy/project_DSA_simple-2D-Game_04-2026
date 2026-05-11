import os
import pygame


class SPIKE:
    """Represents a static environmental hazard with orientation-based collision mechanics."""
    def __init__(self, x, y, width=32, height=32, orientation='up'):
        """Initializes spatial parameters, damage payload, and graphic assets for the hazard.

        Args:
            x (float): The x-coordinate of the tile's top-left origin.
            y (float): The y-coordinate of the tile's top-left origin.
            width (int, optional): The visual width of the spike tile. Defaults to 32.
            height (int, optional): The visual height of the spike tile. Defaults to 32.
            orientation (str, optional): The directional alignment ('up' or 'down'). Defaults to 'up'.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.damage = 1
        self.orientation = orientation

        self.pad_x = 6
        self.pad_y = 10

        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        if self.orientation == 'down':
            img_path = "assets/tiles/spike_downward.png"
        else:
            img_path = "assets/tiles/spike_upward.png"

        if os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            print(f"[SPIKE] ⚠️ Không tìm thấy {img_path}, dùng hình tam giác fallback.")
            self._draw_fallback()

    def _draw_fallback(self):
        """Generates a procedural polygonal representation if the image asset is unavailable."""
        self.image.fill((0, 0, 0, 0))

        if self.orientation == "up":
            points = [
                (self.width // 2, 0),
                (0, self.height),
                (self.width, self.height)
            ]
        else:
            points = [
                (0, 0),
                (self.width, 0),
                (self.width // 2, self.height)
            ]

        pygame.draw.polygon(self.image, (230, 230, 230), points)

    def get_hitbox(self):
        """Computes the precise Axis-Aligned Bounding Box (AABB) taking into account geometric padding.

        Returns:
            pygame.Rect: The internal collision boundary, strictly smaller than the visual tile.
        """
        if self.orientation == 'up':
            hitbox_left = self.x + self.pad_x
            hitbox_right = self.x + self.width - self.pad_x
            hitbox_top = self.y + self.pad_y
            hitbox_bottom = self.y + self.height

        else:
            hitbox_left = self.x + self.pad_x
            hitbox_right = self.x + self.width - self.pad_x
            hitbox_top = self.y
            hitbox_bottom = self.y + self.height - self.pad_y

        return pygame.Rect(
            hitbox_left,
            hitbox_top,
            hitbox_right - hitbox_left,
            hitbox_bottom - hitbox_top
        )

    def check_collision(self, player):
        """Evaluates spatial intersection with a given entity and triggers damage states.

        Args:
            player (object): The entity instance subject to collision and damage resolution.

        Returns:
            bool: True if a hazardous collision occurred, False otherwise.
        """
        hitbox = self.get_hitbox()

        player_rect = pygame.Rect(
            player.x,
            player.y,
            player.width,
            player.height
        )

        if player_rect.colliderect(hitbox):
            if not player.is_invincible:
                player.take_damage(self.damage)
            return True

        return False

    def render(self, screen, camera_x=0.0, camera_y=0.0):
        """Projects the sprite onto the display surface relative to the viewport translation.

        Args:
            screen (pygame.Surface): The primary rendering surface.
            camera_x (float, optional): Viewport horizontal translation. Defaults to 0.0.
            camera_y (float, optional): Viewport vertical translation. Defaults to 0.0.
        """
        draw_x = self.x - camera_x
        draw_y = self.y - camera_y

        screen.blit(self.image, (draw_x, draw_y))