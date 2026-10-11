"""Thực thể Bird với Hitbox chuẩn hóa bất biến và động học bay/rơi."""
from typing import Optional

import arcade
import arcade.hitbox as hb

from ..constants import (
    FLAP_VELOCITY,
    GRAVITY,
    ROT_FLAP,
    ROT_MAX,
    ROT_MIN,
    ROT_VEL,
    STANDARD_HITBOX_HEIGHT,
    STANDARD_HITBOX_WIDTH,
    TERMINAL_VELOCITY,
)


class Bird(arcade.Sprite):
    def __init__(
        self,
        texture: Optional[arcade.Texture] = None,
        scale: float = 1.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        **kwargs,
    ) -> None:
        super().__init__(
            path_or_texture=texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            **kwargs,
        )

        # Chuẩn hóa Hitbox bất biến: cố định 34x24 px bất chấp kích thước texture
        hw = STANDARD_HITBOX_WIDTH / 2.0
        hh = STANDARD_HITBOX_HEIGHT / 2.0
        standard_points = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        self.hit_box = hb.RotatableHitBox(standard_points, position=self.position)

        # Vận tốc theo trục Y
        self.velocity_y: float = 0.0

        # Slot mở rộng cho phụ kiện & hiệu ứng (DX-4)
        self.attachments: dict[str, arcade.Sprite] = {}
        self.trail_enabled: bool = False

    def flap(self) -> None:
        """Thực hiện cú nhảy (vỗ cánh): gán vận tốc hướng lên và ngửa góc."""
        self.velocity_y = FLAP_VELOCITY
        self.angle = ROT_FLAP

    def update_physics(self, dt: float) -> None:
        """Cập nhật trọng lực, tọa độ và góc xoay qua từng bước thời gian dt."""
        # 1. Trọng lực & Giới hạn tốc độ rơi
        self.velocity_y = max(TERMINAL_VELOCITY, self.velocity_y + GRAVITY * dt)
        self.center_y += self.velocity_y * dt

        # 2. Xoay góc (Chúc đầu xuống khi rơi)
        if self.velocity_y < 0:
            self.angle = max(ROT_MIN, min(ROT_MAX, self.angle + ROT_VEL * dt))
        else:
            self.angle = min(ROT_MAX, max(ROT_MIN, self.angle))

        # 3. Đồng bộ tọa độ các phụ kiện đi kèm (nếu có)
        for attachment in self.attachments.values():
            attachment.center_x = self.center_x
            attachment.center_y = self.center_y
            attachment.angle = self.angle

    def reset(self, x: float, y: float) -> None:
        """Đặt lại trạng thái ban đầu của chim."""
        self.center_x = x
        self.center_y = y
        self.velocity_y = 0.0
        self.angle = 0.0
