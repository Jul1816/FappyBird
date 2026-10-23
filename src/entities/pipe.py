"""Pipe entity và PipeManager quản lý các cặp pipe."""
import random
from dataclasses import dataclass
from pathlib import Path

import arcade

from ..constants import (
    ASSETS_DIR,
    FLOOR_HEIGHT,
    PIPE_HORIZONTAL_SPACING,
    PIPE_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class Pipe(arcade.Sprite):
    def __init__(
        self,
        is_upper: bool,
        texture_path: str | Path | arcade.Texture = ASSETS_DIR / "sprites" / "pipe-green.png",
    ) -> None:
        super().__init__(path_or_texture=texture_path)
        self.is_upper = is_upper
        if is_upper:
            # Pipe trên xoay 180 độ
            self.angle = 180.0
        else:
            self.angle = 0.0


@dataclass
class PipePair:
    upper: Pipe
    lower: Pipe
    gap_y: float
    gap_size: float
    scored: bool = False

    @property
    def center_x(self) -> float:
        return self.upper.center_x


class PipeManager:
    def __init__(self, texture_path: str | Path = ASSETS_DIR / "sprites" / "pipe-green.png") -> None:
        self.texture_path = Path(texture_path)
        self.texture: arcade.Texture = arcade.load_texture(self.texture_path)
        self.sprite_list = arcade.SpriteList()
        self.pairs: list[PipePair] = []

    def can_spawn(self) -> bool:
        """Check khoảng cách pipe gần nhất đã đủ điều kiện spawn pipe mới chưa."""
        if not self.pairs:
            return True
        last_pipe = self.pairs[-1]
        return (SCREEN_WIDTH - last_pipe.center_x) >= PIPE_HORIZONTAL_SPACING

    def spawn(self, gap_size: float) -> PipePair:
        """Spawn cặp pipe mới tại mép phải màn hình với gap_size."""
        # Clamp an toàn cho gap_y giữa floor và trần màn hình
        min_gap_y = FLOOR_HEIGHT + 30.0 + gap_size / 2.0
        max_gap_y = SCREEN_HEIGHT - 30.0 - gap_size / 2.0
        gap_y = random.uniform(min_gap_y, max_gap_y)

        spawn_x = SCREEN_WIDTH + PIPE_WIDTH / 2.0

        upper = Pipe(is_upper=True, texture_path=self.texture)
        upper.center_x = spawn_x
        upper.bottom = gap_y + gap_size / 2.0

        lower = Pipe(is_upper=False, texture_path=self.texture)
        lower.center_x = spawn_x
        lower.top = gap_y - gap_size / 2.0

        pair = PipePair(upper=upper, lower=lower, gap_y=gap_y, gap_size=gap_size)
        self.pairs.append(pair)
        self.sprite_list.append(upper)
        self.sprite_list.append(lower)
        return pair

    def update(self, dt: float, world_speed: float) -> None:
        """Update di chuyển pipe và cleanup các pipe đã ra khỏi viewport."""
        dx = world_speed * dt
        for pipe in self.sprite_list:
            pipe.center_x -= dx

        # Cleanup các pipe pair đã vượt qua mép trái
        surviving_pairs: list[PipePair] = []
        for pair in self.pairs:
            if pair.upper.right < 0:
                pair.upper.remove_from_sprite_lists()
                pair.lower.remove_from_sprite_lists()
            else:
                surviving_pairs.append(pair)
        self.pairs = surviving_pairs

    def check_score(self, bird_x: float) -> int:
        """Check score khi bird vượt qua pipe pair chưa ghi điểm."""
        points = 0
        for pair in self.pairs:
            if not pair.scored and bird_x >= pair.center_x:
                pair.scored = True
                points += 1
        return points

    def reset(self) -> None:
        """Clear toàn bộ pipe trong sprite list và pair list."""
        self.sprite_list.clear()
        self.pairs.clear()
