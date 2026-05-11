# NAMELESS CAT PROJECT: SOURCE CODE DOCUMENTATION

## File: `settings.py`
---

## File: `ui.py`
---
### Class: `UI`
**Description:**
```text
Manages the Heads-Up Display (HUD) and graphical overlay states for the game.
```

#### Method: `__init__`
**Description:**
```text
Initializes viewport dimensions and typography resources for UI rendering.

Args:
    screen_width (int): The horizontal resolution of the display window.
    screen_height (int): The vertical resolution of the display window.
```

#### Method: `draw_health_bar`
**Description:**
```text
Renders discrete hit-point indicators to represent the player's current vitality.

Args:
    screen (pygame.Surface): The primary display surface to render the HUD on.
    current_hp (int): The player's active health points.
    max_hp (int, optional): The maximum health capacity. Defaults to 3.
```

#### Method: `draw_game_over`
**Description:**
```text
Projects a semi-transparent overlay and state-transition prompts for the end-game sequence.

Args:
    screen (pygame.Surface): The primary display surface.
```

### Class: `ImageButton`
**Description:**
```text
Represents an interactive graphical user interface (GUI) component with sprite scaling.
```

#### Method: `__init__`
**Description:**
```text
Initializes the button's visual representation and spatial bounding box.

Args:
    x (float): The x-coordinate for the center of the button.
    y (float): The y-coordinate for the center of the button.
    image (pygame.Surface): The base graphical asset for the button.
    scale (float, optional): The uniform scaling multiplier. Defaults to 1.0.
```

#### Method: `draw`
**Description:**
```text
Renders the button sprite onto the designated display surface.

Args:
    screen (pygame.Surface): The primary rendering surface.
```

#### Method: `is_clicked`
**Description:**
```text
Evaluates pointer-based interaction within the button's collision domain.

Args:
    event (pygame.event.Event): The input event queued by Pygame.

Returns:
    bool: True if a left mouse click intersects the bounding box, False otherwise.
```


## File: `camera.py`
---
### Class: `Camera`
**Description:**
```text
Manage camera scrolling based on a target within level boundaries.
```

#### Method: `__init__`
**Description:**
```text
Initialize the camera with screen dimensions.

Args:
    screen_width (int): Width of the display screen in pixels.
    screen_height (int): Height of the display screen in pixels.
```

#### Method: `get_target_center`
**Description:**
```text
Get the center position of a target object.

Args:
    target (object): Object whose position is determined from rect,
        hitbox, collision_rect, x/y/width/height, or x/y attributes.

Returns:
    tuple[int, int]: The x and y coordinates of the target center.

Raises:
    AttributeError: If the target does not contain supported position attributes.
```

#### Method: `update`
**Description:**
```text
Update camera scrolling to follow a target within level boundaries.

Args:
    target (object): Object followed by the camera.
    level_width (int): Total width of the level in pixels.
    level_height (int): Total height of the level in pixels.
```


## File: `level.py`
---
### Class: `LEVEL`
**Description:**
```text
Load, parse, and render a 2D level from an LDtk map file.
```

#### Method: `__init__`
**Description:**
```text
Initialize the level data, assets, and parse the LDtk file.

Args:
    ldtk_filepath (str): Path to the LDtk JSON file used to load the level.
```

#### Method: `parse_ldtk`
**Description:**
```text
Parse an LDtk JSON file and extract level geometry and entities.

Args:
    filepath (str): Path to the LDtk JSON file.

Raises:
    FileNotFoundError: If the LDtk file does not exist.
    RuntimeError: If the file cannot be read, contains no levels,
        or has invalid map dimensions.
```

#### Method: `_parse_blocks`
**Description:**
```text
Parse the block layer into collision rectangles and renderable tiles.

Args:
    layer (dict): LDtk IntGrid layer containing block and tile data.

Raises:
    RuntimeError: If the block layer grid width is invalid.
```

#### Method: `_parse_entities`
**Description:**
```text
Parse entity spawn points from an LDtk entity layer.

Args:
    layer (dict): LDtk Entities layer containing player, portal,
        and enemy spawn data.
```

#### Method: `render`
**Description:**
```text
Render the level surface to the screen using camera scroll offsets.

Args:
    screen (pygame.Surface): Target display surface.
    scroll_x (int): Horizontal camera scroll offset.
    scroll_y (int): Vertical camera scroll offset.

Raises:
    RuntimeError: If the level surface has not been created.
```


## File: `entity.py`
---
### Class: `ENTITY`
**Description:**
```text
Represent a base movable and interactive game entity.

This class provides common attributes and methods for position, velocity,
animation, rendering, and tile-based collision handling.
```

#### Method: `__init__`
**Description:**
```text
Initialize the entity position, size, motion, and animation state.

Args:
    x (float): Initial x-coordinate of the entity.
    y (float): Initial y-coordinate of the entity.
    width (int): Width of the entity collision box.
    height (int): Height of the entity collision box.
```

#### Method: `extract_frames`
**Description:**
```text
Extract a sequence of animation frames from a sprite sheet row.

Args:
    row (int): Row index in the sprite sheet.
    num_frames (int): Number of frames to extract.
    frame_size (tuple[int, int]): Width and height of each frame.

Returns:
    list[pygame.Surface]: List of processed animation frames.
```

#### Method: `extract_custom_frames`
**Description:**
```text
Extract specific animation frames from sprite sheet coordinates.

Args:
    frame_coords (list[tuple[int, int]]): List of frame positions as
        row and column pairs.
    frame_size (tuple[int, int]): Width and height of each frame.

Returns:
    list[pygame.Surface]: List of processed animation frames.
```

#### Method: `_process_frame`
**Description:**
```text
Crop, trim, and scale a frame from the sprite sheet.

Args:
    x (int): Source x-coordinate of the frame.
    y (int): Source y-coordinate of the frame.
    w (int): Width of the frame.
    h (int): Height of the frame.

Returns:
    pygame.Surface | None: Processed frame surface, or None if processing fails.
```

#### Method: `update_animations`
**Description:**
```text
Update the current animation frame based on the entity state.

Advances the animation timer using the configured speed and loops the
animation when it reaches the final frame.
```

#### Method: `render`
**Description:**
```text
Render the entity image to the screen with camera offset.

Args:
    screen (pygame.Surface): Target surface used for rendering.
    camera_x (float): Horizontal camera offset.
    camera_y (float): Vertical camera offset.
```

#### Method: `get_nearby_platforms`
**Description:**
```text
Retrieve nearby platforms using spatial grid coordinates.

Args:
    spatial_platforms (dict[tuple[int, int], pygame.Rect]): Dictionary
        mapping tile coordinates to platform rectangles.
    tile_size (int): Size of each tile in pixels.

Returns:
    list[pygame.Rect]: Platforms located near the entity.
```

#### Method: `handle_vertical_collision`
**Description:**
```text
Resolve vertical AABB collisions with nearby platforms.

Updates the vertical position, resets vertical velocity on collision,
and sets the grounded state when the entity lands on a platform.

Args:
    spatial_platforms (dict[tuple[int, int], pygame.Rect]): Dictionary
        mapping tile coordinates to platform rectangles.
```

#### Method: `handle_horizontal_collision`
**Description:**
```text
Resolve horizontal AABB collisions with nearby platforms.

Updates the horizontal position and prevents the entity from passing
through platform boundaries.

Args:
    spatial_platforms (dict[tuple[int, int], pygame.Rect]): Dictionary
        mapping tile coordinates to platform rectangles.
```


## File: `player.py`
---
### Class: `PLAYER`
**Description:**
```text
Represent the main controllable player character.

The player handles keyboard input, movement physics, animation updates,
health management, damage invincibility, and rendering.
```

#### Method: `__init__`
**Description:**
```text
Initialize the player entity, movement attributes, and animations.

Args:
    x (float): Initial x-coordinate of the player in world space.
    y (float): Initial y-coordinate of the player in world space.
    width (int): Width of the player's collision box.
    height (int): Height of the player's collision box.
```

#### Method: `update`
**Description:**
```text
Update player input, movement physics, invincibility, and animation.

Applies gravity, limits falling speed, processes keyboard movement,
handles jumping, and advances the current animation frame.
```

#### Method: `take_damage`
**Description:**
```text
Apply damage to the player and activate temporary invincibility.

Args:
    amount (int): Amount of health points to subtract from the player.
```

#### Method: `render`
**Description:**
```text
Render the player sprite with camera offset and invincibility effect.

Args:
    screen (pygame.Surface): Target surface used for rendering.
    camera_x (float): Horizontal camera scroll offset.
    camera_y (float): Vertical camera scroll offset.
```


## File: `portal.py`
---
### Class: `PORTAL`
**Description:**
```text
Represents a portal entity for spatial transitions within the game environment.
```

#### Method: `__init__`
**Description:**
```text
Initializes the portal's spatial dimensions and visual properties.

Args:
    x (float): The x-coordinate of the portal's top-left corner.
    y (float): The y-coordinate of the portal's top-left corner.
    width (int, optional): The bounding box width in pixels. Defaults to 64.
    height (int, optional): The bounding box height in pixels. Defaults to 64.
```

#### Method: `check_collision`
**Description:**
```text
Evaluates Axis-Aligned Bounding Box (AABB) collision between the portal and the player.

Args:
    player (object): The player entity instance. Must possess 'x', 'y', 'width', and 'height' attributes.

Returns:
    bool: True if bounding boxes intersect, False otherwise.
```

#### Method: `render`
**Description:**
```text
Renders the portal onto the display surface with a time-based oscillating alpha effect.

Args:
    screen (pygame.Surface): The primary display surface to render the portal on.
    scroll_x (float): The current horizontal camera offset.
    scroll_y (float): The current vertical camera offset.
```


## File: `projectile.py`
---
### Class: `PROJECTILE`
**Description:**
```text
Represents a dynamic projectile entity with kinematic behavior and animated sprites.
```

#### Method: `__init__`
**Description:**
```text
Initializes the projectile's physical properties, payload, and visual assets.

Args:
    x (float): The initial x-coordinate of the projectile.
    y (float): The initial y-coordinate of the projectile.
    vx (float): Horizontal velocity component.
    vy (float): Vertical velocity component.
    damage (int, optional): The damage payload delivered upon impact. Defaults to 1.
    max_range (int, optional): Maximum travel distance before despawning. Defaults to 400.
```

#### Method: `update`
**Description:**
```text
Processes the projectile's kinematics, sprite rotation, and environmental collision.

Args:
    tiles (dict/set): A collection of static grid coordinates representing obstacles.
```

#### Method: `render`
**Description:**
```text
Projects the visual representation onto the 2D viewport.

Args:
    screen (pygame.Surface): The primary display surface.
    camera_x (float): The current horizontal camera translation offset.
    camera_y (float): The current vertical camera translation offset.
```


## File: `spikes.py`
---
### Class: `SPIKE`
**Description:**
```text
Represents a static environmental hazard with orientation-based collision mechanics.
```

#### Method: `__init__`
**Description:**
```text
Initializes spatial parameters, damage payload, and graphic assets for the hazard.

Args:
    x (float): The x-coordinate of the tile's top-left origin.
    y (float): The y-coordinate of the tile's top-left origin.
    width (int, optional): The visual width of the spike tile. Defaults to 32.
    height (int, optional): The visual height of the spike tile. Defaults to 32.
    orientation (str, optional): The directional alignment ('up' or 'down'). Defaults to 'up'.
```

#### Method: `_draw_fallback`
**Description:**
```text
Generates a procedural polygonal representation if the image asset is unavailable.
```

#### Method: `get_hitbox`
**Description:**
```text
Computes the precise Axis-Aligned Bounding Box (AABB) taking into account geometric padding.

Returns:
    pygame.Rect: The internal collision boundary, strictly smaller than the visual tile.
```

#### Method: `check_collision`
**Description:**
```text
Evaluates spatial intersection with a given entity and triggers damage states.

Args:
    player (object): The entity instance subject to collision and damage resolution.

Returns:
    bool: True if a hazardous collision occurred, False otherwise.
```

#### Method: `render`
**Description:**
```text
Projects the sprite onto the display surface relative to the viewport translation.

Args:
    screen (pygame.Surface): The primary rendering surface.
    camera_x (float, optional): Viewport horizontal translation. Defaults to 0.0.
    camera_y (float, optional): Viewport vertical translation. Defaults to 0.0.
```


## File: `chase_enemy.py`
---
### Class: `CHASE_ENEMY`
**Description:**
```text
Represents an advanced hostile entity featuring line-of-sight detection, state-driven chasing, and melee attack mechanics.
```

#### Method: `__init__`
**Description:**
```text
Initializes the entity's kinematic base, perception thresholds, and state-dependent animation assets.

Args:
    x (float): Initial x-coordinate and patrol anchor.
    y (float): Initial y-coordinate.
    width (int): Bounding box width.
    height (int): Bounding box height.
    patrol_distance (float, optional): Maximum lateral patrol deviation. Defaults to 300.0.
    hp (int, optional): Maximum health points. Defaults to 5.
    damage (int, optional): Damage payload delivered upon attack phase. Defaults to 2.
```

#### Method: `check_player_interactions`
**Description:**
```text
Evaluates spatial intersections and line-of-sight heuristics to transition between patrol, chase, and attack states.

Args:
    player (object): The player entity subject to vision tracking and collision detection.
```

#### Method: `update`
**Description:**
```text
Advances the entity's kinematic logic, state-machine behavioral branching, and sprite animations per logical frame.
```


## File: `enemy_base.py`
---
### Class: `ENEMY_BASE`
**Description:**
```text
Abstract base class for hostile entities, managing kinematics, spatial awareness, and combat resolution.
```

#### Method: `__init__`
**Description:**
```text
Initializes foundational attributes for the enemy entity.

Args:
    x (float): The initial x-coordinate of the entity.
    y (float): The initial y-coordinate of the entity.
    width (int): Bounding box width.
    height (int): Bounding box height.
    hp (int, optional): Maximum health points. Defaults to 3.
    damage (int, optional): Damage payload delivered upon contact. Defaults to 1.
```

#### Method: `check_player_interactions`
**Description:**
```text
Evaluates AABB intersection with the player, applying damage and kinetic knockback.

Args:
    player (object): The player entity instance to check against.
```

#### Method: `handle_horizontal_collision`
**Description:**
```text
Resolves lateral displacement against environmental constraints via raycasting and edge detection.

Args:
    spatial_platforms (list/dict): A collection of platform bounds for spatial queries.
```

#### Method: `apply_gravity`
**Description:**
```text
Applies continuous downward acceleration bounded by terminal velocity.
```

#### Method: `update`
**Description:**
```text
Advances the kinematic state of the entity per logical frame.
```


## File: `patrol_enemy.py`
---
### Class: `PATROL_ENEMY`
**Description:**
```text
Represents a hostile entity with an automated, distance-bounded oscillating patrol routine.
```

#### Method: `__init__`
**Description:**
```text
Initializes the patrolling entity's kinematic properties, spatial anchors, and visual assets.

Args:
    x (float): The initial x-coordinate, serving as the central anchor for the patrol route.
    y (float): The initial y-coordinate.
    width (int): Bounding box width.
    height (int): Bounding box height.
    patrol_distance (float, optional): The maximum lateral deviation from the starting anchor. Defaults to 150.0.
    hp (int, optional): Maximum health points. Defaults to 4.
    damage (int, optional): Damage payload delivered upon contact. Defaults to 2.
```

#### Method: `update`
**Description:**
```text
Processes the entity's frame-by-frame state, strictly enforcing spatial patrol boundaries.
```


## File: `ranged_aiming.py`
---
### Class: `AIMING_ENEMY`
**Description:**
```text
Represents an aerial hostile entity with sinusoidal hovering mechanics and vector-based projectile targeting.
```

#### Method: `__init__`
**Description:**
```text
Initializes combat parameters, floating constraints, and projectile reservoirs.

Args:
    x (float): Initial x-coordinate.
    y (float): Initial y-coordinate.
    width (int): Bounding box width.
    height (int): Bounding box height.
    hp (int, optional): Maximum health points. Defaults to 2.
    damage (int, optional): Contact damage payload. Defaults to 1.
```

#### Method: `update`
**Description:**
```text
Computes sinusoidal vertical displacement and advances the kinematic state of active projectiles.

Args:
    tiles (list, optional): Environmental grid segments for projectile collision resolution. Defaults to None.
```

#### Method: `check_player_interactions`
**Description:**
```text
Resolves projectile-entity intersections and evaluates line-of-sight vector magnitude for attack triggering.

Args:
    player (object): The target entity for collision and targeting heuristics.
```

#### Method: `shoot`
**Description:**
```text
Normalizes the directional vector towards the target to instantiate and propel a projectile.

Args:
    dist_x (float): The horizontal scalar distance to the target.
    dist_y (float): The vertical scalar distance to the target.
```

#### Method: `render`
**Description:**
```text
Projects the entity and its localized projectile pool onto the viewport.

Args:
    screen (pygame.Surface): The primary display surface.
    camera_x (float): Viewport horizontal translation.
    camera_y (float): Viewport vertical translation.
```


## File: `ranged_horizontal.py`
---
### Class: `RANGED_HORIZONTAL`
**Description:**
```text
Represents a ranged hostile entity capable of horizontal projectile emission based on proximity-triggered aggression.
```

#### Method: `__init__`
**Description:**
```text
Initializes combat attributes, projectile reservoirs, and temporal cooldown parameters.

Args:
    x (float): Initial x-coordinate.
    y (float): Initial y-coordinate.
    width (int): Bounding box width.
    height (int): Bounding box height.
    hp (int, optional): Maximum health points. Defaults to 3.
    damage (int, optional): Contact damage payload. Defaults to 1.
```

#### Method: `shoot`
**Description:**
```text
Instantiates and propels a projectile along the horizontal axis aligned with the entity's current orientation.
```

#### Method: `update`
**Description:**
```text
Advances the kinematic state of the entity and processes spatial updates for all active projectiles.

Args:
    tiles (list, optional): Environmental grid constraints for projectile collision. Defaults to None.
```

#### Method: `check_player_interactions`
**Description:**
```text
Evaluates projectile intersections and triggers temporal-based firing sequences within specific spatial boundaries.

Args:
    player (object): The target entity for collision resolution and proximity detection.
```

#### Method: `render`
**Description:**
```text
Projects the entity and its active projectiles onto the 2D viewport.

Args:
    screen (pygame.Surface): The primary display surface.
    camera_x (float): Viewport horizontal translation.
    camera_y (float): Viewport vertical translation.
```


