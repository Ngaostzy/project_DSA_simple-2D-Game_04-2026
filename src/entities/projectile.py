import pygame
import math 

class PROJECTILE:
    """Represents a dynamic projectile entity with kinematic behavior and animated sprites."""
    def __init__(self, x, y, vx, vy, damage=1, max_range=400):
        """Initializes the projectile's physical properties, payload, and visual assets.

        Args:
            x (float): The initial x-coordinate of the projectile.
            y (float): The initial y-coordinate of the projectile.
            vx (float): Horizontal velocity component.
            vy (float): Vertical velocity component.
            damage (int, optional): The damage payload delivered upon impact. Defaults to 1.
            max_range (int, optional): Maximum travel distance before despawning. Defaults to 400.
        """
        self.x = x
        self.y = y
        
        self.width = 24 
        self.height = 24
        
        self.vx = vx
        self.vy = vy
        self.damage = damage
        
        self.is_dead = False
        self.distance_travel = 0
        self.max_range = max_range
 
        self.animations = []
        self.current_frame = 0
        self.animation_speed = 0.2 
        
        self.has_sprite = False

        try:
            sprite_sheet = pygame.image.load("assets/sprites/bat.png").convert_alpha()
            sheet_w, sheet_h = sprite_sheet.get_size()
            frame_w = sheet_w // 16 
            frame_h = sheet_h 
            
            for i in range(16):
                frame_rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
                frame_image = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                frame_image.blit(sprite_sheet, (0, 0), frame_rect)
                
                scale_factor = 1.5 
                final_w = int(frame_w * scale_factor)
                final_h = int(frame_h * scale_factor)
                frame_image = pygame.transform.scale(frame_image, (final_w, final_h))
                
                self.animations.append(frame_image)
            
            self.image = self.animations[0]
            self.width = int(final_w * 0.8) 
            self.height = int(final_h * 0.8)
            self.has_sprite = True

        except FileNotFoundError:
            print("WARNING: Không tìm thấy file 'bat.png'. Dùng cục vuông thay thế.")
            self.image = None
    def update(self, tiles):
        """Processes the projectile's kinematics, sprite rotation, and environmental collision.

        Args:
            tiles (dict/set): A collection of static grid coordinates representing obstacles.
        """
        if self.is_dead: return

        self.x += self.vx
        self.y += self.vy
        
        self.distance_travel += math.hypot(self.vx, self.vy)

        if self.has_sprite and self.animations:
            self.current_frame += self.animation_speed
            if self.current_frame >= len(self.animations):
                self.current_frame = 0
            
            base_image = self.animations[int(self.current_frame)]

            angle = math.degrees(math.atan2(-self.vy, self.vx))
            
            self.image = pygame.transform.rotate(base_image, angle)

        if self.distance_travel > self.max_range:
            self.is_dead = True
            return

        grid_size = 32
        bullet_col = int(self.x //grid_size)
        bullet_row = int(self.y // grid_size)

        if (bullet_col, bullet_row) in tiles:
            self.is_dead = True
            return

    def render(self, screen, camera_x, camera_y):
        """Projects the visual representation onto the 2D viewport.

        Args:
            screen (pygame.Surface): The primary display surface.
            camera_x (float): The current horizontal camera translation offset.
            camera_y (float): The current vertical camera translation offset.
        """
        if self.is_dead: return
        
        if self.has_sprite and self.image:
            rot_rect = self.image.get_rect()
            rot_rect.center = (int(self.x - camera_x), int(self.y - camera_y))
            
            screen.blit(self.image, rot_rect.topleft)
            
        else:
            pygame.draw.rect(screen, (255, 200, 0), (int(self.x - camera_x), int(self.y - camera_y), 10, 10))