"""Định nghĩa dữ liệu Skin và danh mục skin mặc định."""
from dataclasses import dataclass
from typing import Literal

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

    @property
    def is_free(self) -> bool:
        return self.unlock_type == "default"


# Danh mục 5 skin khởi tạo
DEFAULT_SKINS: list[Skin] = [
    Skin(
        id="classic",
        name="Vàng Cổ Điển",
        price=0,
        unlock_type="default",
        unlock_value=0,
        sprite_path="assets/skins/classic.png",
        description="Chú chim màu vàng huyền thoại.",
    ),
    Skin(
        id="blue_bird",
        name="Chim Xanh Dương",
        price=10,
        unlock_type="coin",
        unlock_value=10,
        sprite_path="assets/skins/blue_bird.png",
        description="Chú chim xanh nhanh nhẹn (10 Coins).",
    ),
    Skin(
        id="red_bird",
        name="Chim Lửa Đỏ",
        price=25,
        unlock_type="coin",
        unlock_value=25,
        sprite_path="assets/skins/red_bird.png",
        description="Chú chim đỏ dũng mãnh (25 Coins).",
    ),
    Skin(
        id="cyber_bird",
        name="Chim Cơ Khí",
        price=0,
        unlock_type="highscore",
        unlock_value=20,
        sprite_path="assets/skins/cyber_bird.png",
        description="Mở khóa khi đạt High Score >= 20.",
    ),
    Skin(
        id="golden_bird",
        name="Chim Hoàng Kim",
        price=0,
        unlock_type="total_coins",
        unlock_value=50,
        sprite_path="assets/skins/golden_bird.png",
        description="Mở khóa khi tích lũy tổng cộng >= 50 Coins.",
    ),
]
