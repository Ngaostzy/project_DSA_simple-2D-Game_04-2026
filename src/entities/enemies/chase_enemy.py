import pygame
from src.entities.enemies.patrol_enemy import PATROL_ENEMY

class CHASE_ENEMY(PATROL_ENEMY):
    """Represents an advanced hostile entity featuring line-of-sight detection, state-driven chasing, and melee attack mechanics."""
    def __init__(self, x, y, width, height, patrol_distance=300.0, hp=5, damage=2):
        """Initializes the entity's kinematic base, perception thresholds, and state-dependent animation assets.

        Args:
            x (float): Initial x-coordinate and patrol anchor.
            y (float): Initial y-coordinate.
            width (int): Bounding box width.
            height (int): Bounding box height.
            patrol_distance (float, optional): Maximum lateral patrol deviation. Defaults to 300.0.
            hp (int, optional): Maximum health points. Defaults to 5.
            damage (int, optional): Damage payload delivered upon attack phase. Defaults to 2.
        """
        super().__init__(x, y, width, height, patrol_distance, hp, damage)
        
        self.normal_speed = 1.5
        self.chase_speed = 3.5
        
        self.patrol_vision_x = 200
        self.patrol_vision_y = 50
        self.chase_vision_x = 400
        self.chase_vision_y = 250
        self.max_chase_dist = 350 
        
        self.is_chasing = False
        self.ignore_player_timer = 0
        self.state = 'walk'
        self.scale_factor = 2.7 

        try:
            self.animation_speeds = {'walk': 0.18, 'attack': 0.25} 
            f_size = (100, 100) 
            
            self.sprite_sheet = pygame.image.load("assets/sprites/Orc_Walk.png").convert_alpha()
            self.animations['walk'] = self.extract_frames(row=0, num_frames=8, frame_size=f_size)
            
            self.sprite_sheet = pygame.image.load("assets/sprites/Orc_Attack.png").convert_alpha()
            self.animations['attack'] = self.extract_frames(row=0, num_frames=6, frame_size=f_size)

            self.image = self.animations['walk'][0]
            
        except FileNotFoundError:
            print("WARNING: Thiếu file Orc_Walk.png hoặc Orc_Attack.png!")

    def check_player_interactions(self, player):
        """Evaluates spatial intersections and line-of-sight heuristics to transition between patrol, chase, and attack states.

        Args:
            player (object): The player entity subject to vision tracking and collision detection.
        """
        if self.is_dead: return

        if (player.x < self.x + self.width and
            player.x + player.width > self.x and
            player.y < self.y + self.height and
            player.y + player.height > self.y):
            
            if self.state != 'attack':
                self.state = 'attack'
                self.current_frame = 0 

            super(PATROL_ENEMY, self).check_player_interactions(player)

        if getattr(self, 'ignore_player_timer', 0) > 0:
            self.ignore_player_timer -= 1
            self.speed = self.normal_speed
            self.is_chasing = False
            return

        dist_x = player.x - self.x
        dist_y = player.y - self.y
        player_dist_from_home = abs(player.x - self.start_x)

        if not self.is_chasing:
            is_in_front = (self.facing_right and dist_x > 0) or (not self.facing_right and dist_x < 0)
            if is_in_front and abs(dist_x) < self.patrol_vision_x and abs(dist_y) < self.patrol_vision_y:
                self.is_chasing = True 
        else:
            if (abs(dist_x) > self.chase_vision_x or 
                abs(dist_y) > self.chase_vision_y or 
                player_dist_from_home > self.max_chase_dist):
                self.is_chasing = False 

        if self.is_chasing:
            self.speed = self.chase_speed
            if self.is_grounded and self.state != 'attack':
                self.facing_right = dist_x > 0
        else:
            self.speed = self.normal_speed

    def update(self):
        """Advances the entity's kinematic logic, state-machine behavioral branching, and sprite animations per logical frame."""
        super(PATROL_ENEMY, self).update()

        if self.state == 'attack':
            self.vel_x = 0 
            
            self.current_frame += self.animation_speeds.get('attack', 0.1)
            if self.current_frame >= len(self.animations['attack']):
                self.current_frame = 0
                self.state = 'walk' 
            else:
                self.image = self.animations['attack'][int(self.current_frame)]
                
        else:
            if getattr(self, 'ignore_player_timer', 0) > 0:
                self.vel_x = self.speed if self.facing_right else -self.speed
            elif self.is_chasing:
                self.vel_x = self.speed if self.facing_right else -self.speed
            else:
                if self.facing_right:
                    self.vel_x = self.speed
                    if self.x >= self.start_x + self.patrol_distance:
                        self.facing_right = False
                else:
                    self.vel_x = -self.speed
                    if self.x <= self.start_x - self.patrol_distance:
                        self.facing_right = True

            self.state = 'walk'
            self.current_frame += self.animation_speeds.get('walk', 0.18)
            if self.current_frame >= len(self.animations['walk']):
                self.current_frame = 0
            self.image = self.animations['walk'][int(self.current_frame)]