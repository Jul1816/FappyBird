"""Định nghĩa dữ liệu Skin và danh mục skin mặc định."""
from dataclasses import dataclass
from typing import Literal

from ..constants import ASSETS_DIR

UnlockType = Literal["default", "coin", "highscore", "total_coins"]


@dataclass(frozen=True)
class Skin:
    id: str
    name: str
    price: int
    unlock_type: UnlockType
    unlock_value: int
    sprite_path: str
    description: str = ""


# Danh mục 6 skin khởi tạo
DEFAULT_SKINS: list[Skin] = [
    Skin(
        id="classic",
        name="Classic Yellow",
        price=0,
        unlock_type="default",
        unlock_value=0,
        sprite_path=str(ASSETS_DIR / "skins" / "classic.png"),
        description="The legendary yellow bird.",
    ),
    Skin(
        id="blue_bird",
        name="Swift Blue",
        price=10,
        unlock_type="coin",
        unlock_value=10,
        sprite_path=str(ASSETS_DIR / "skins" / "blue_bird.png"),
        description="Agile blue flyer (10 Coins).",
    ),
    Skin(
        id="red_bird",
        name="Fiery Red",
        price=25,
        unlock_type="coin",
        unlock_value=25,
        sprite_path=str(ASSETS_DIR / "skins" / "red_bird.png"),
        description="Bold red champion (25 Coins).",
    ),
    Skin(
        id="cyber_bird",
        name="Cyber Bird",
        price=0,
        unlock_type="highscore",
        unlock_value=20,
        sprite_path=str(ASSETS_DIR / "skins" / "cyber_bird.png"),
        description="Unlock at High Score >= 20.",
    ),
    Skin(
        id="golden_bird",
        name="Golden Bird",
        price=0,
        unlock_type="total_coins",
        unlock_value=50,
        sprite_path=str(ASSETS_DIR / "skins" / "golden_bird.png"),
        description="Unlock at Total Coins >= 50.",
    ),
    Skin(
        id="custom_robin",
        name="Angel Robin",
        price=0,
        unlock_type="default",
        unlock_value=0,
        sprite_path=str(ASSETS_DIR / "skins" / "custom_robin.png"),
        description="Custom skin: Angel Robin auto-fit to 24px.",
    ),
]

