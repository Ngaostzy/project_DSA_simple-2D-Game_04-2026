# NAMELESS CAT PROJECT: SOURCE CODE DOCUMENTATION

## File: `settings.py`
---

## File: `camera.py`
---
### Class: `Camera`
**Description:**
```text
Manages the viewport camera for smooth horizontal scrolling.

This class tracks and calculates the horizontal offset required to keep 
a target entity (typically the player) focused on the display screen.
```

#### Method: `__init__`
**Description:**
```text
Initializes the Camera with a default horizontal scroll offset.
```

#### Method: `update`
**Description:**
```text
Updates the camera's horizontal offset to follow the target.

Applies a smooth scrolling algorithm (linear interpolation) by moving
the camera a fraction of the distance toward the target's center, 
rather than snapping to it instantly.

Args:
    target (Entity): The entity to track. Must possess an 'x' 
                     coordinate attribute (e.g., the Player object).
```


## File: `level.py`
---
### Class: `LEVEL`
**Description:**
```text
Handles the loading, parsing, and rendering of game levels based on CSV data.

This class reads a 2D matrix from a CSV file exported by Tiled Map Editor,
converts the grid data into physical game objects (Obstacles), and stores
them in a dynamic array for collision detection and rendering.

Attributes:
    platforms (list): A dynamic array containing all Obstacle entities in the level.
```

#### Method: `__init__`
**Description:**
```text
Initializes the Level object and triggers the map loading process.

Args:
    csv_filepath (str): The relative or absolute path to the map's CSV file.
```

#### Method: `load_map`
**Description:**
```text
Parses a CSV file and instantiates Obstacle objects based on grid coordinates.

The algorithm iterates through the 2D matrix. Empty spaces ('0' or '-1') 
are ignored. Solid tiles generate an Obstacle whose world coordinates are 
calculated by multiplying its matrix indices (row, col) by TILE_SIZE.

Args:
    filepath (str): The path to the CSV file to be read.

Raises:
    FileNotFoundError: If the provided filepath does not exist.
```

#### Method: `render`
**Description:**
```text
Renders all platforms in the level relative to the camera's viewport.

Args:
    screen (pygame.Surface): The main display surface to draw on.
    camera_x (float): The current horizontal scroll offset of the camera.
```


## File: `entity.py`
---
### Class: `ENTITY`
**Description:**
```text
Base class for all movable and interactive objects in the game.

Provides foundational attributes for spatial positioning, dimensions, 
and velocity. It is designed to be inherited by specific game objects 
(e.g., Player, Enemies) which will override the base methods.
```

#### Method: `__init__`
**Description:**
```text
Initializes the entity's spatial and kinematic properties.

Args:
    x (float): The initial horizontal coordinate (top-left).
    y (float): The initial vertical coordinate (top-left).
    width (int): The logical width of the entity's bounding box.
    height (int): The logical height of the entity's bounding box.
```

#### Method: `update`
**Description:**
```text
Updates the internal state, physics, and logic of the entity.

This method acts as an interface and is intended to be overridden 
by subclasses to implement specific behaviors (e.g., applying gravity, 
handling inputs, or advancing animations).
```

#### Method: `render`
**Description:**
```text
Draws the entity onto the display surface.

This method acts as an interface and is intended to be overridden 
by subclasses to handle specific rendering logic, such as drawing 
sprites and applying camera offsets.

Args:
    screen (pygame.Surface): The main display surface to draw on.
```


## File: `obstacle.py`
---
### Class: `OBSTACLE`
**Description:**
```text
Represents a static environmental object within the game world.

Obstacles serve as physical boundaries, platforms, or floors that dynamic 
entities (such as the Player or Enemies) can stand on and collide with.
```

#### Method: `__init__`
**Description:**
```text
Initializes the obstacle with spatial dimensions and visual properties.

Args:
    x (float): The horizontal coordinate of the top-left corner.
    y (float): The vertical coordinate of the top-left corner.
    width (int): The physical width of the obstacle.
    height (int): The physical height of the obstacle.
```

#### Method: `render`
**Description:**
```text
Draws the obstacle onto the display surface relative to the camera.

Calculates the screen-space position by applying the camera's horizontal 
offset to the world coordinates, ensuring the obstacle scrolls correctly 
with the environment.

Args:
    screen (pygame.Surface): The main display surface to draw on.
    camera_x (float, optional): The horizontal scroll offset of the camera. Defaults to 0.0.
```


## File: `player.py`
---
### Class: `PLAYER`
**Description:**
```text
The main player character, inheriting from Entity.

Attributes:
    image (pygame.Surface): The graphical representation of the player.
    jump_power (float): The upward velocity applied when jumping.
    is_grounded (bool): State flag indicating if the player is resting on a surface.
```

#### Method: `__init__`
**Description:**
```text
Initializes the player entity and loads its sprite.

Args:
    x (float): Initial X coordinate in world space.
    y (float): Initial Y coordinate in world space.
    width (int): Width of the character's bounding box.
    height (int): Height of the character's bounding box.
```

#### Method: `extract_frames`
**Description:**
```text
Extracts and scales individual frames from the sprite sheet.

This method slices out a specific number of frames 
from a given row on the sprite sheet, scaling them up, and
storing them in a list for animation sequencing.

Args:
    row (int): The row index on the sprite sheet containing the animation (0-indexed).
    num_frames (int): The total number of frames to extract from that row.

Returns:
    list: A list of scaled pygame.Surface objects representing the animation frames.
```

#### Method: `update`
**Description:**
```text
Updates player physics and handles keyboard inputs
and advances the animation.
Args: None
Return: None
```

#### Method: `render`
**Description:**
```text
Draws the player's sprite onto the screen surface.
Calculates the relative screen position based on the camera offset and
flips the sprite horizontally if the player is facing left.

Args:
    screen (pygame.Surface): The main display surface.
    camera_x (float): The current horizontal scroll offset of the camera.
```


