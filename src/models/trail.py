"""Định nghĩa dữ liệu Trail và danh mục vệt bay mặc định."""
from dataclasses import dataclass
from typing import Literal

from ..constants import ASSETS_DIR
from .skin import UnlockType

TrailType = Literal["none", "particle", "ghost"]


@dataclass(frozen=True)
class Trail:
    id: str
    name: str
    trail_type: TrailType
    unlock_type: UnlockType
    unlock_value: int
    price: int
    sprite_path: str = ""
    color_tint: tuple[int, int, int] = (255, 255, 255)
    description: str = ""


# Thư mục sprite chứa các hạt vệt bay
TRAILS_SPRITES_DIR = ASSETS_DIR / "sprites" / "trails"

# Danh mục 7 trail khởi tạo
DEFAULT_TRAILS: list[Trail] = [
    Trail(
        id="none",
        name="No Trail",
        trail_type="none",
        unlock_type="default",
        unlock_value=0,
        price=0,
        description="No trail effect.",
    ),
    Trail(
        id="custom",
        name="Custom Trail",
        trail_type="particle",
        unlock_type="default",
        unlock_value=0,
        price=0,
        sprite_path=str(TRAILS_SPRITES_DIR / "custom_trail.png"),
        description="Custom sprite trail from assets.",
    ),
    Trail(
        id="ghost",
        name="Ghost Echo",
        trail_type="ghost",
        unlock_type="highscore",
        unlock_value=15,
        price=0,
        color_tint=(255, 255, 255),
        description="Unlock at High Score >= 15.",
    ),
    Trail(
        id="star",
        name="Star Dust",
        trail_type="particle",
        unlock_type="coin",
        unlock_value=15,
        price=15,
        sprite_path=str(TRAILS_SPRITES_DIR / "star.png"),
        description="Shining star dust (15 Coins).",
    ),
    Trail(
        id="heart",
        name="Love Flutter",
        trail_type="particle",
        unlock_type="coin",
        unlock_value=25,
        price=25,
        sprite_path=str(TRAILS_SPRITES_DIR / "heart.png"),
        description="Fluttering hearts (25 Coins).",
    ),
    Trail(
        id="fire",
        name="Fiery Spark",
        trail_type="particle",
        unlock_type="highscore",
        unlock_value=40,
        price=0,
        sprite_path=str(TRAILS_SPRITES_DIR / "fire.png"),
        description="Unlock at High Score >= 40.",
    ),
    Trail(
        id="shadow",
        name="Shadow Phantom",
        trail_type="ghost",
        unlock_type="total_coins",
        unlock_value=80,
        price=0,
        color_tint=(138, 43, 226),
        description="Unlock at Total Coins >= 80.",
    ),
]
