"""Bird entity với standard fixed hitbox và flight/gravity physics."""
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
        scale: Optional[float] = None,
        center_x: float = 0.0,
        center_y: float = 0.0,
        **kwargs,
    ) -> None:
        # Auto-scale theo chiều cao chuẩn STANDARD_HITBOX_HEIGHT (24.0 px)
        if scale is None:
            if texture is not None and getattr(texture, "height", 0) > 0:
                scale = STANDARD_HITBOX_HEIGHT / float(texture.height)
            else:
                scale = 1.0

        super().__init__(
            path_or_texture=texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            **kwargs,
        )

        # Chuẩn hóa hitbox cố định 34x24 px bất chấp texture size
        hw = STANDARD_HITBOX_WIDTH / 2.0
        hh = STANDARD_HITBOX_HEIGHT / 2.0
        standard_points = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        self.hit_box = hb.RotatableHitBox(standard_points, position=self.position)

        # Y velocity
        self.velocity_y: float = 0.0

    def set_skin_texture(self, texture: Optional[arcade.Texture]) -> None:
        """Update skin texture cho Bird và auto-scale tương ứng."""
        if texture is not None:
            self.texture = texture
            if getattr(texture, "height", 0) > 0:
                self.scale = STANDARD_HITBOX_HEIGHT / float(texture.height)
            else:
                self.scale = 1.0

            # Reset hitbox chuẩn 34x24 px quanh origin (0, 0)
            hw = STANDARD_HITBOX_WIDTH / 2.0
            hh = STANDARD_HITBOX_HEIGHT / 2.0
            standard_points = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
            self.hit_box = hb.RotatableHitBox(standard_points, position=self.position)
        else:
            self.scale = 1.0

    def flap(self) -> None:
        """Thực hiện flap: set positive Y velocity và ngửa góc xoay."""
        self.velocity_y = FLAP_VELOCITY
        self.angle = ROT_FLAP

    def update_physics(self, dt: float) -> None:
        """Update physics (gravity, vị trí Y, rotation angle) theo dt."""
        # 1. Apply gravity & clamp terminal velocity
        self.velocity_y = max(TERMINAL_VELOCITY, self.velocity_y + GRAVITY * dt)
        self.center_y += self.velocity_y * dt

        # 2. Rotate angle (dive angle khi rơi)
        if self.velocity_y < 0:
            self.angle = max(ROT_MIN, min(ROT_MAX, self.angle + ROT_VEL * dt))
        else:
            self.angle = min(ROT_MAX, max(ROT_MIN, self.angle))
