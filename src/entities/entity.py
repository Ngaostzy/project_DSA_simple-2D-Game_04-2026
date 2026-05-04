import pygame
class ENTITY:
    """
    Base class for all movable and interactive objects in the game.

    Provides foundational attributes for spatial positioning, dimensions, 
    and velocity. It is designed to be inherited by specific game objects 
    (e.g., Player, Enemies) which will override the base methods.
    """
    def __init__(self, x, y, width, height):
        """
        Initializes the entity's spatial and kinematic properties.

        Args:
            x (float): The initial horizontal coordinate (top-left).
            y (float): The initial vertical coordinate (top-left).
            width (int): The logical width of the entity's bounding box.
            height (int): The logical height of the entity's bounding box.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vel_x = 0.0
        self.vel_y = 0.0

        self.sprite_sheet = None
        self.animations = {}
        self.animation_speeds = {}
        self.state = 'idle'
        self.current_frame = 0.0
        self.image = None
        self.scale_factor = 1
        self.facing_right = True
    
    def extract_frames(self, row, num_frames, frame_size=(32, 32)):
        """Utility to extract a continuous row of frames."""
        frames = []
        f_width, f_height = frame_size
        
        for col in range(num_frames):
            x_cut, y_cut = col * f_width, row * f_height
            frame = self._process_frame(x_cut, y_cut, f_width, f_height)
            if frame: frames.append(frame)
        return frames
    
    def extract_custom_frames(self, frame_coords : list, frame_size=(32,32)):
        """Utility to extract specific frames from coordinates (row, col)."""
        frames = []
        f_width, f_height = frame_size
        for row, col in frame_coords:
            x_cut, y_cut = col * f_width, row * f_height
            frame = self._process_frame(x_cut, y_cut, f_width, f_height)
            if frame: frames.append(frame)
        return frames
    
    def _process_frame(self, x, y, w, h):
        """Internal helper for cropping and scaling."""
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
        """
        Updates the internal state, physics, and logic of the entity.

        This method acts as an interface and is intended to be overridden 
        by subclasses to implement specific behaviors (e.g., applying gravity, 
        handling inputs, or advancing animations).
        """
        if self.state in self.animations:
            anim_list = self.animations[self.state]
            speed = self.animation_speeds.get(self.state, 0.1)
            self.current_frame += speed
            if self.current_frame >= len(anim_list):
                self.current_frame = 0
            self.image = anim_list[int(self.current_frame)]


    def render(self, screen: pygame.surface, camera_x = 0.0):
        """
        Draws the entity onto the display surface.

        This method acts as an interface and is intended to be overridden 
        by subclasses to handle specific rendering logic, such as drawing 
        sprites and applying camera offsets.

        Args:
            screen (pygame.Surface): The main display surface to draw on.
        """
        if not self.image: return
        offset_y = self.height - self.image.get_height()
        offset_x = (self.width - self.image.get_width())/2

        draw_x = self.x - camera_x + offset_x
        draw_y = self.y + offset_y

        img_to_draw = self.image
        if not self.facing_right:
            img_to_draw = pygame.transform.flip(self.image, True, False)
        
        screen.blit(img_to_draw, (draw_x, draw_y))
