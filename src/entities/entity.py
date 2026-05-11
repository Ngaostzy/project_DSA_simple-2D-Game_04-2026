import pygame
class ENTITY:

    """Represent a base movable and interactive game entity.

    This class provides common attributes and methods for position, velocity,
    animation, rendering, and tile-based collision handling.
    """

    def __init__(self, x, y, width, height):

        """Initialize the entity position, size, motion, and animation state.

        Args:
            x (float): Initial x-coordinate of the entity.
            y (float): Initial y-coordinate of the entity.
            width (int): Width of the entity collision box.
            height (int): Height of the entity collision box.
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vel_x = 0.0
        self.vel_y = 0.0
        self.is_grounded = False

        self.sprite_sheet = None
        self.animations = {}
        self.animation_speeds = {}
        self.state = 'idle'
        self.current_frame = 0.0
        self.image = None
        self.scale_factor = 1
        self.facing_right = True
    
    def extract_frames(self, row, num_frames, frame_size=(32, 32)):

        """Extract a sequence of animation frames from a sprite sheet row.

        Args:
            row (int): Row index in the sprite sheet.
            num_frames (int): Number of frames to extract.
            frame_size (tuple[int, int]): Width and height of each frame.

        Returns:
            list[pygame.Surface]: List of processed animation frames.
        """

        frames = []
        f_width, f_height = frame_size
        
        for col in range(num_frames):
            x_cut, y_cut = col * f_width, row * f_height
            frame = self._process_frame(x_cut, y_cut, f_width, f_height)
            if frame: frames.append(frame)
        return frames
    
    def extract_custom_frames(self, frame_coords : list, frame_size=(32,32)):

        """Extract specific animation frames from sprite sheet coordinates.

        Args:
            frame_coords (list[tuple[int, int]]): List of frame positions as
                row and column pairs.
            frame_size (tuple[int, int]): Width and height of each frame.

        Returns:
            list[pygame.Surface]: List of processed animation frames.
        """

        frames = []
        f_width, f_height = frame_size
        for row, col in frame_coords:
            x_cut, y_cut = col * f_width, row * f_height
            frame = self._process_frame(x_cut, y_cut, f_width, f_height)
            if frame: frames.append(frame)
        return frames
    
    def _process_frame(self, x, y, w, h):

        """Crop, trim, and scale a frame from the sprite sheet.

        Args:
            x (int): Source x-coordinate of the frame.
            y (int): Source y-coordinate of the frame.
            w (int): Width of the frame.
            h (int): Height of the frame.

        Returns:
            pygame.Surface | None: Processed frame surface, or None if processing fails.
        """

        try:
            frame_ref = self.sprite_sheet.subsurface((x, y, w, h))
            frame_surface = frame_ref.copy()
            bounding_rect = frame_surface.get_bounding_rect()
            cropped = frame_surface.subsurface(bounding_rect)
            return pygame.transform.scale_by(cropped, self.scale_factor)
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None


    def update_animations(self):

        """Update the current animation frame based on the entity state.

        Advances the animation timer using the configured speed and loops the
        animation when it reaches the final frame.
        """

        if self.state in self.animations:
            anim_list = self.animations[self.state]
            speed = self.animation_speeds.get(self.state, 0.1)
            self.current_frame += speed
            if self.current_frame >= len(anim_list):
                self.current_frame = 0
            self.image = anim_list[int(self.current_frame)]


    def render(self, screen: pygame.surface, camera_x = 0.0, camera_y = 0.0):
 
        """Render the entity image to the screen with camera offset.

        Args:
            screen (pygame.Surface): Target surface used for rendering.
            camera_x (float): Horizontal camera offset.
            camera_y (float): Vertical camera offset.
        """

        if not self.image: return
        offset_y = self.height - self.image.get_height()
        offset_x = (self.width - self.image.get_width())/2

        draw_x = self.x - camera_x + offset_x
        draw_y = self.y - camera_y + offset_y

        img_to_draw = self.image
        if not self.facing_right:
            img_to_draw = pygame.transform.flip(self.image, True, False)
        
        screen.blit(img_to_draw, (draw_x, draw_y))
    
    def get_nearby_platforms(self, spatial_platforms, tile_size = 32):

        """Retrieve nearby platforms using spatial grid coordinates.

        Args:
            spatial_platforms (dict[tuple[int, int], pygame.Rect]): Dictionary
                mapping tile coordinates to platform rectangles.
            tile_size (int): Size of each tile in pixels.

        Returns:
            list[pygame.Rect]: Platforms located near the entity.
        """

        nearby_platforms = []

        start_col = int(self.x // tile_size) - 1
        end_col = int((self.x + self.width) // tile_size ) +1

        start_row = int(self.y // tile_size)
        end_row = int((self.y + self.height) // tile_size) + 4
        
        for col in range(start_col, end_col+1):
            for row in range(start_row, end_row+1):
                if (col, row) in spatial_platforms:
                    nearby_platforms.append(spatial_platforms[(col, row)])
        
        return nearby_platforms

    def handle_vertical_collision(self, spatial_platforms):

        """Resolve vertical AABB collisions with nearby platforms.

        Updates the vertical position, resets vertical velocity on collision,
        and sets the grounded state when the entity lands on a platform.

        Args:
            spatial_platforms (dict[tuple[int, int], pygame.Rect]): Dictionary
                mapping tile coordinates to platform rectangles.
        """

        self.y += self.vel_y
        self.is_grounded = False

        nearby = self.get_nearby_platforms(spatial_platforms)

        for plat in nearby:
            if self.x + self.width > plat.x and self.x < plat.x + plat.width:
                if self.y + self.height > plat.y and self.y < plat.y + plat.height:

                    if self.vel_y > 0:
                        self.y = plat.y - self.height 
                        self.is_grounded = True
                    elif self.vel_y < 0:
                        self.y = plat.y +plat.height 

                    self.vel_y = 0
                    break

    def handle_horizontal_collision(self, spatial_platforms):

        """Resolve horizontal AABB collisions with nearby platforms.

        Updates the horizontal position and prevents the entity from passing
        through platform boundaries.

        Args:
            spatial_platforms (dict[tuple[int, int], pygame.Rect]): Dictionary
                mapping tile coordinates to platform rectangles.
        """

        self.x += self.vel_x

        if self.vel_x == 0:
            return
        
        nearby = self.get_nearby_platforms(spatial_platforms)

        for plat in nearby:
            if self.y + self.height > plat.y and self.y < plat.y + plat.height:
                if self.x + self.width > plat.x and self.x < plat.x + plat.width:
                    if self.vel_x > 0:
                        self.x = plat.x - self.width
                    elif self.vel_x < 0:
                        self.x = plat.x + plat.width
                    
                    self.vel_x = 0 
                    break
                
                
                
