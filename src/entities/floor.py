"""Floor entity với cơ chế seamless scrolling loop."""
import arcade

from ..constants import ASSETS_DIR, FLOOR_HEIGHT


class Floor(arcade.Sprite):
    def __init__(self, texture_path: str = str(ASSETS_DIR / "sprites" / "base.png")) -> None:
        super().__init__(path_or_texture=texture_path)
        # base.png kích thước 336x112, pattern loop mỗi 16 px
        self.pattern_repeat: float = 16.0
        self.scroll_offset: float = 0.0
        self.reset()

    def update_scroll(self, dt: float, world_speed: float) -> None:
        """Scroll floor sang trái theo pattern 16px liền mạch, tránh hở gap."""
        self.scroll_offset = (self.scroll_offset + world_speed * dt) % self.pattern_repeat
        self.left = -self.scroll_offset

    def reset(self) -> None:
        """Reset vị trí floor về tọa độ ban đầu."""
        self.scroll_offset = 0.0
        self.left = 0.0
        self.top = FLOOR_HEIGHT
