"""Thực thể quản lý hiệu ứng vệt bay (Trail Emitter, Particle & Ghost Snapshot)."""
import random
from typing import Optional

import arcade

from ..constants import ASSETS_DIR
from ..models.trail import Trail


class TrailParticle(arcade.Sprite):
    """Hạt vệt bay di chuyển với vận tốc (vx, vy), tuổi thọ cố định và alpha mờ dần."""

    def __init__(
        self,
        texture: Optional[arcade.Texture] = None,
        scale: float = 1.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        vx: float = 0.0,
        vy: float = 0.0,
        life: float = 0.45,
        max_alpha: int = 220,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(
            path_or_texture=texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
        )
        self.vx = vx
        self.vy = vy
        self.life = max(0.01, life)
        self.max_alpha = max_alpha
        self.age = 0.0
        self.color = (color[0], color[1], color[2], max_alpha)

    def update_particle(self, dt: float) -> bool:
        """Cập nhật tọa độ và độ trong suốt. Trả về False nếu hạt đã hết hạn."""
        self.age += dt
        if self.age >= self.life:
            return False

        self.center_x += self.vx * dt
        self.center_y += self.vy * dt

        progress = min(1.0, self.age / self.life)
        new_alpha = int(self.max_alpha * (1.0 - progress))
        cur_rgb = self.color[:3]
        self.color = (cur_rgb[0], cur_rgb[1], cur_rgb[2], max(0, new_alpha))
        return True


class GhostSnapshot(arcade.Sprite):
    """Bóng ma chụp lại hình dáng, tỷ lệ scale và góc nghiêng của chim, trôi lùi theo thế giới."""

    def __init__(
        self,
        texture: Optional[arcade.Texture] = None,
        scale: float = 1.0,
        center_x: float = 0.0,
        center_y: float = 0.0,
        angle: float = 0.0,
        vx: float = 0.0,
        life: float = 0.35,
        max_alpha: int = 160,
        color_tint: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(
            path_or_texture=texture,
            scale=scale,
            center_x=center_x,
            center_y=center_y,
            angle=angle,
        )
        self.vx = vx
        self.life = max(0.01, life)
        self.max_alpha = max_alpha
        self.age = 0.0
        self.color = (color_tint[0], color_tint[1], color_tint[2], max_alpha)

    def update_ghost(self, dt: float) -> bool:
        """Cập nhật độ mờ dần và vị trí trôi ngang. Trả về False khi hết hạn."""
        self.age += dt
        if self.age >= self.life:
            return False

        self.center_x += self.vx * dt

        progress = min(1.0, self.age / self.life)
        new_alpha = int(self.max_alpha * (1.0 - progress))
        cur_rgb = self.color[:3]
        self.color = (cur_rgb[0], cur_rgb[1], cur_rgb[2], max(0, new_alpha))
        return True


class TrailEmitter:
    """Quản lý sinh hạt, vòng đời và vẽ các hiệu ứng vệt bay (Particle & Ghost)."""

    MAX_PARTICLES: int = 50
    EMIT_INTERVAL: float = 0.06

    def __init__(self) -> None:
        self.particles = arcade.SpriteList()
        self.current_trail: Optional[Trail] = None
        self.particle_texture: Optional[arcade.Texture] = None
        self.particle_scale: float = 1.0
        self.emit_timer: float = 0.0

    def calculate_auto_scale(self, texture: Optional[arcade.Texture]) -> float:
        """Chuẩn hóa kích thước hạt theo Bounding Box (cạnh lớn nhất nằm trong khung 14x14 px)."""
        if not texture:
            return 1.0
        w = float(getattr(texture, "width", 14.0) or 14.0)
        h = float(getattr(texture, "height", 14.0) or 14.0)
        max_dim = max(1.0, max(w, h))
        return 14.0 / max_dim

    def set_trail(self, trail: Optional[Trail]) -> None:
        """Chuyển đổi sang cấu hình vệt bay mới và nạp trước texture hạt nếu cần."""
        self.current_trail = trail
        self.clear()
        self.emit_timer = 0.0
        self.particle_texture = None
        self.particle_scale = 1.0

        if not trail or trail.trail_type == "none":
            return

        if trail.trail_type == "particle":
            try:
                self.particle_texture = arcade.load_texture(trail.sprite_path)
            except Exception:
                try:
                    self.particle_texture = arcade.load_texture(ASSETS_DIR / "sprites" / "trails" / "star.png")
                except Exception:
                    self.particle_texture = None

            if trail.id == "custom":
                self.particle_scale = self.calculate_auto_scale(self.particle_texture)
            else:
                self.particle_scale = 1.0

    def _add_particle(self, sprite: arcade.Sprite) -> None:
        """Thêm hạt mới vào danh sách kèm chính sách FIFO (giải phóng hạt cũ nhất khi vượt ngưỡng 50)."""
        while len(self.particles) >= self.MAX_PARTICLES:
            oldest = self.particles[0]
            oldest.remove_from_sprite_lists()
        self.particles.append(sprite)

    def update(
        self,
        dt: float,
        world_speed: float,
        bird_x: float,
        bird_y: float,
        bird_angle: float,
        bird_texture: Optional[arcade.Texture],
        bird_scale: float = 1.0,
    ) -> None:
        """Cập nhật toàn bộ hạt hiện có và sinh hạt mới theo định kỳ khi bay."""
        # 1. Cập nhật các hạt / bóng ma đang sống
        for p in list(self.particles):
            if isinstance(p, TrailParticle):
                if not p.update_particle(dt):
                    p.remove_from_sprite_lists()
            elif isinstance(p, GhostSnapshot):
                if not p.update_ghost(dt):
                    p.remove_from_sprite_lists()

        # 2. Sinh hạt mới nếu đang trang bị trail hoạt động
        if not self.current_trail or self.current_trail.trail_type == "none":
            return

        self.emit_timer += dt
        if self.emit_timer >= self.EMIT_INTERVAL:
            self.emit_timer = 0.0
            spawn_x = bird_x - 14.0
            spawn_y = bird_y + random.uniform(-3.0, 3.0)

            if self.current_trail.trail_type == "particle" and self.particle_texture:
                vx = -world_speed + random.uniform(-10.0, 10.0)
                vy = self._get_vertical_velocity(self.current_trail.id)
                particle = TrailParticle(
                    texture=self.particle_texture,
                    scale=self.particle_scale,
                    center_x=spawn_x,
                    center_y=spawn_y,
                    vx=vx,
                    vy=vy,
                    life=0.45,
                    max_alpha=220,
                    color=self.current_trail.color_tint,
                )
                self._add_particle(particle)

            elif self.current_trail.trail_type == "ghost" and bird_texture:
                ghost = GhostSnapshot(
                    texture=bird_texture,
                    scale=bird_scale,
                    center_x=bird_x,
                    center_y=bird_y,
                    angle=bird_angle,
                    vx=-world_speed,
                    life=0.35,
                    max_alpha=150,
                    color_tint=self.current_trail.color_tint,
                )
                self._add_particle(ghost)

    def burst(
        self,
        bird_x: float,
        bird_y: float,
        bird_angle: float,
        bird_texture: Optional[arcade.Texture],
        bird_scale: float = 1.0,
        world_speed: float = 180.0,
    ) -> None:
        """Kích hoạt phản hồi lực bùng nổ chùm hạt tức thì khi chim vỗ cánh (flap)."""
        if not self.current_trail or self.current_trail.trail_type == "none":
            return

        spawn_x = bird_x - 14.0

        if self.current_trail.trail_type == "particle" and self.particle_texture:
            for _ in range(4):
                spawn_y = bird_y + random.uniform(-5.0, 5.0)
                vx = -world_speed + random.uniform(-20.0, 5.0)
                vy = self._get_vertical_velocity(self.current_trail.id) + random.uniform(-15.0, 15.0)
                particle = TrailParticle(
                    texture=self.particle_texture,
                    scale=self.particle_scale,
                    center_x=spawn_x,
                    center_y=spawn_y,
                    vx=vx,
                    vy=vy,
                    life=random.uniform(0.35, 0.48),
                    max_alpha=240,
                    color=self.current_trail.color_tint,
                )
                self._add_particle(particle)

        elif self.current_trail.trail_type == "ghost" and bird_texture:
            ghost = GhostSnapshot(
                texture=bird_texture,
                scale=bird_scale,
                center_x=bird_x,
                center_y=bird_y,
                angle=bird_angle,
                vx=-world_speed,
                life=0.38,
                max_alpha=180,
                color_tint=self.current_trail.color_tint,
            )
            self._add_particle(ghost)

    def _get_vertical_velocity(self, trail_id: str) -> float:
        """Tính vận tốc dọc phù hợp với từng chủ đề hạt."""
        if trail_id == "fire":
            return random.uniform(20.0, 50.0)
        elif trail_id == "heart":
            return random.uniform(5.0, 25.0)
        elif trail_id == "star":
            return random.uniform(-15.0, 15.0)
        else:  # custom
            return random.uniform(-10.0, 20.0)

    def draw(self) -> None:
        """Vẽ toàn bộ hạt qua batch draw của SpriteList."""
        self.particles.draw()

    def clear(self) -> None:
        """Dọn dẹp sạch sẽ toàn bộ hạt trên màn hình."""
        self.particles.clear()
