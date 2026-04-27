import csv
import pygame 
from src.settings import *
from src.entities.obstacle import OBSTACLE

class LEVEL:
    """
    Handles the loading, parsing, and rendering of game levels based on CSV data.

    This class reads a 2D matrix from a CSV file exported by Tiled Map Editor,
    converts the grid data into physical game objects (Obstacles), and stores
    them in a dynamic array for collision detection and rendering.

    Attributes:
        platforms (list): A dynamic array containing all Obstacle entities in the level.
    """
    def __init__(self, csv_filepath):
        """
        Initializes the Level object and triggers the map loading process.

        Args:
            csv_filepath (str): The relative or absolute path to the map's CSV file.
        """
        self.platforms = []
        self.load_map(csv_filepath)
    def load_map(self, filepath):
        """
        Parses a CSV file and instantiates Obstacle objects based on grid coordinates.

        The algorithm iterates through the 2D matrix. Empty spaces ('0' or '-1') 
        are ignored. Solid tiles generate an Obstacle whose world coordinates are 
        calculated by multiplying its matrix indices (row, col) by TILE_SIZE.

        Args:
            filepath (str): The path to the CSV file to be read.

        Raises:
            FileNotFoundError: If the provided filepath does not exist.
        """
        try:
            with open(filepath, newline= '', encoding="utf-8") as file:
                reader = csv.reader(file)
                for row_index, row in enumerate(reader):
                    for col_index, val in enumerate(row):
                        if val == '0'or val == '-1' or val == '':
                            continue
                        if val != '0':
                            x = col_index * TILE_SIZE
                            y = row_index * TILE_SIZE
                            self.platforms.append(OBSTACLE(x, y, TILE_SIZE, TILE_SIZE))
        except FileNotFoundError:
            print(f"ERROR: Map undefined at {filepath}")
    def render(self, screen, camera_x):
        """
        Renders all platforms in the level relative to the camera's viewport.

        Args:
            screen (pygame.Surface): The main display surface to draw on.
            camera_x (float): The current horizontal scroll offset of the camera.
        """
        for plat in self.platforms:
            plat.render(screen, camera_x)

