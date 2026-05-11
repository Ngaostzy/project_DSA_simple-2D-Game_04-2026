class Camera:
    """Manage camera scrolling based on a target within level boundaries."""
    def __init__(self, screen_width, screen_height):
        """Initialize the camera with screen dimensions.

        Args:
            screen_width (int): Width of the display screen in pixels.
            screen_height (int): Height of the display screen in pixels.
        """
        self.scroll_y = 0
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_target_center(self, target):

        """Get the center position of a target object.

        Args:
            target (object): Object whose position is determined from rect,
                hitbox, collision_rect, x/y/width/height, or x/y attributes.

        Returns:
            tuple[int, int]: The x and y coordinates of the target center.

        Raises:
            AttributeError: If the target does not contain supported position attributes.
        """
        if hasattr(target, "rect"):
            return target.rect.centerx, target.rect.centery

        if hasattr(target, "hitbox"):
            return target.hitbox.centerx, target.hitbox.centery

        if hasattr(target, "collision_rect"):
            return target.collision_rect.centerx, target.collision_rect.centery

        if all(hasattr(target, attr) for attr in ["x", "y", "width", "height"]):
            return (
                target.x + target.width // 2,
                target.y + target.height // 2
            )

        if hasattr(target, "x") and hasattr(target, "y"):
            return target.x, target.y

        raise AttributeError(
            "Camera không tìm được vị trí của target. "
            "Target cần có rect, hitbox, collision_rect hoặc x/y."
        )

    def update(self, target, level_width, level_height):

        """Update camera scrolling to follow a target within level boundaries.

        Args:
            target (object): Object followed by the camera.
            level_width (int): Total width of the level in pixels.
            level_height (int): Total height of the level in pixels.
        """

        target_center_x, target_center_y = self.get_target_center(target)

        self.scroll_x = target_center_x - self.screen_width // 2
        self.scroll_y = target_center_y - self.screen_height // 2

        max_scroll_x = max(0, level_width - self.screen_width)
        max_scroll_y = max(0, level_height - self.screen_height)

        self.scroll_x = max(0, min(self.scroll_x, max_scroll_x))
        self.scroll_y = max(0, min(self.scroll_y, max_scroll_y))

        self.scroll_x = int(self.scroll_x)
        self.scroll_y = int(self.scroll_y)