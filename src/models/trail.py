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


# Thư mục sprite chứa các hạt vệt bay (ngang hàng với skins)
TRAILS_SPRITES_DIR = ASSETS_DIR / "trails"

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
        id="money",
        name="Money",
        trail_type="particle",
        unlock_type="coin",
        unlock_value=50,
        price=50,
        sprite_path=str(TRAILS_SPRITES_DIR / "money.png"),
        description="Paper wealth flutter (50 Coins).",
    ),
    Trail(
        id="heart",
        name="Heart",
        trail_type="particle",
        unlock_type="coin",
        unlock_value=25,
        price=25,
        sprite_path=str(TRAILS_SPRITES_DIR / "heart.png"),
        description="Fluttering hearts (25 Coins).",
    ),
    Trail(
        id="fiery",
        name="Fiery",
        trail_type="particle",
        unlock_type="highscore",
        unlock_value=40,
        price=0,
        sprite_path=str(TRAILS_SPRITES_DIR / "fiery.png"),
        description="Unlock at High Score >= 40.",
    ),
    Trail(
        id="primo",
        name="Primo",
        trail_type="particle",
        unlock_type="coin",
        unlock_value=70,
        price=70,
        sprite_path=str(TRAILS_SPRITES_DIR / "primo.png"),
        description="Genshin wishes spark (70 Coins).",
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
