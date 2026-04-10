class ENTITY:
    """
    Base class for all entities in the game.
    """
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        """
        Update the internal state and game logic of the entities.
        """
        pass
    def render(self, screen):
        """
        Renders the entities onto the given screen surface.
        """

        pass
