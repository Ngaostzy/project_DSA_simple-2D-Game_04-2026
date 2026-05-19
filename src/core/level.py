import json
import os
import pygame


class LEVEL:
    """Load, parse, and render a 2D level from an LDtk map file."""
    def __init__(self, ldtk_filepath):
        """Initialize the level data, assets, and parse the LDtk file.

        Args:
            ldtk_filepath (str): Path to the LDtk JSON file used to load the level.
        """

        self.tile_size = 32
        self.width = 0
        self.height = 0

        self.platforms = []

        self.spatial_platforms = {}

        self.spawn_points = {
            "Player": (100, 100),
            "Portal": (0, 0),
            "Enemies": []
        }

        self.map_surface = None
        self.block_img = None
        self.tileset_img = None

        block_path = "assets/tiles/block.png"
        if os.path.exists(block_path):
            self.block_img = pygame.image.load(block_path).convert_alpha()
            self.block_img = pygame.transform.scale(
                self.block_img,
                (self.tile_size, self.tile_size)
            )
        else:
            print("[LEVEL] ! Không tìm thấy assets/tiles/block.png, sẽ vẽ block bằng rect màu.")

        tileset_path = "assets/tiles/tile_set_3_1.png"
        if os.path.exists(tileset_path):
            self.tileset_img = pygame.image.load(tileset_path).convert_alpha()
            print("[LEVEL] Đã load tileset:", tileset_path)
        else:
            print("[LEVEL] ! Không tìm thấy assets/tiles/tile_set_3_1.png, dùng block fallback.")

        self.parse_ldtk(ldtk_filepath)


    def parse_ldtk(self, filepath):
        """Parse an LDtk JSON file and extract level geometry and entities.

        Args:
            filepath (str): Path to the LDtk JSON file.

        Raises:
            FileNotFoundError: If the LDtk file does not exist.
            RuntimeError: If the file cannot be read, contains no levels,
                or has invalid map dimensions.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"[LEVEL] Không tìm thấy file LDtk: {filepath}")

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data = json.load(file)
        except Exception as e:
            raise RuntimeError(f"[LEVEL] Lỗi khi đọc file LDtk: {e}")

        if "levels" not in data or len(data["levels"]) == 0:
            raise RuntimeError("[LEVEL] File LDtk không có level nào.")

        level_data = data["levels"][0]

        blocks_layer = None

        for layer in level_data.get("layerInstances", []):
            if layer.get("__identifier") == "Blocks":
                blocks_layer = layer
                break

        if blocks_layer is not None:
            grid_size = blocks_layer.get("__gridSize", self.tile_size)
            grid_w = blocks_layer.get("__cWid", 0)
            grid_h = blocks_layer.get("__cHei", 0)

            self.tile_size = grid_size
            self.width = grid_w * grid_size
            self.height = grid_h * grid_size
        else:
            self.width = level_data.get("pxWid", 0)
            self.height = level_data.get("pxHei", 0)

        if self.width <= 0 or self.height <= 0:
            raise RuntimeError("[LEVEL] Kích thước map không hợp lệ.")

        self.map_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for layer in level_data.get("layerInstances", []):
            layer_type = layer.get("__type")
            layer_name = layer.get("__identifier")

            if layer_type == "IntGrid" and layer_name == "Blocks":
                self._parse_blocks(layer)

            elif layer_type == "Entities":
                self._parse_entities(layer)

    def _parse_blocks(self, layer):

        """Parse the block layer into collision rectangles and renderable tiles.

        Args:
            layer (dict): LDtk IntGrid layer containing block and tile data.

        Raises:
            RuntimeError: If the block layer grid width is invalid.
        """

        grid_size = layer.get("__gridSize", self.tile_size)
        grid_width = layer.get("__cWid", 0)
        offset_x = layer.get("__pxTotalOffsetX", 0)
        offset_y = layer.get("__pxTotalOffsetY", 0)

        if grid_width <= 0:
            raise RuntimeError("[LEVEL] Blocks layer có __cWid không hợp lệ.")

        int_grid = layer.get("intGridCsv", [])

        if len(int_grid) > 0 and len(int_grid) % grid_width != 0:
            raise RuntimeError(f"[DATA CORRUPTED] Data integrity error: The length of the 1D array ({len(int_grid)}) does not match the map width ({grid_width}). The JSON file may have been tampered with!")

        for index, value in enumerate(int_grid):
            if value > 0:
                col = index % grid_width
                row = index // grid_width
                x = col * grid_size + offset_x
                y = row * grid_size + offset_y
                rect = pygame.Rect(x, y, grid_size, grid_size)
                self.platforms.append(rect)

                self.spatial_platforms[(col, row)] = rect

        tiles = layer.get("autoLayerTiles", [])

        for tile in tiles:
            px_x, px_y = tile.get("px", [0, 0])
            draw_x = px_x + offset_x
            draw_y = px_y + offset_y

            if self.tileset_img is not None and "src" in tile:
                src_x, src_y = tile["src"]

                self.map_surface.blit(
                    self.tileset_img,
                    (draw_x, draw_y),
                    pygame.Rect(src_x, src_y, grid_size, grid_size)
                )

            elif self.block_img is not None:
                self.map_surface.blit(self.block_img, (draw_x, draw_y))

            else:
                pygame.draw.rect(
                    self.map_surface,
                    (90, 25, 25),
                    pygame.Rect(draw_x, draw_y, grid_size, grid_size)
                )

    def _parse_entities(self, layer):

        """Parse entity spawn points from an LDtk entity layer.

        Args:
            layer (dict): LDtk Entities layer containing player, portal,
                and enemy spawn data.
        """

        for entity in layer.get("entityInstances", []):
            name = entity.get("__identifier", "")
            x, y = entity.get("px", [0, 0])

            width = entity.get("width", self.tile_size)
            height = entity.get("height", self.tile_size)
            pivot = entity.get("__pivot", [0, 0])

            actual_x = x - (width * pivot[0])
            actual_y = y - (height * pivot[1])

            if name == "Player":
                self.spawn_points["Player"] = (actual_x, actual_y)

            elif name == "Portal":
                self.spawn_points["Portal"] = (actual_x, actual_y)

            else:
                self.spawn_points["Enemies"].append((name, actual_x, actual_y))

    def render(self, screen, scroll_x, scroll_y):

        """Render the level surface to the screen using camera scroll offsets.

        Args:
            screen (pygame.Surface): Target display surface.
            scroll_x (int): Horizontal camera scroll offset.
            scroll_y (int): Vertical camera scroll offset.

        Raises:
            RuntimeError: If the level surface has not been created.
        """
        if self.map_surface is None:
            raise RuntimeError("[LEVEL] map_surface chưa được tạo. Có thể parse_ldtk đã lỗi.")

        screen.blit(self.map_surface, (-scroll_x, -scroll_y))