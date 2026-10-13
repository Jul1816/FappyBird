"""Unit tests verifying authentic retro assets in RGBA format and Nearest-Neighbor texture filtering."""
from pathlib import Path
from PIL import Image
import pytest

from src.constants import ASSETS_DIR


def test_authentic_assets_exist_and_are_rgba():
    """Tất cả các sprite môi trường, UI, font số và skin phải tồn tại ở định dạng RGBA với kích thước chuẩn."""
    expected_assets = {
        ASSETS_DIR / "sprites" / "background-day.png": (288, 512),
        ASSETS_DIR / "sprites" / "background-night.png": (288, 512),
        ASSETS_DIR / "sprites" / "base.png": (336, 112),
        ASSETS_DIR / "sprites" / "pipe-green.png": (52, 320),
        ASSETS_DIR / "sprites" / "pipe-red.png": (52, 320),
        ASSETS_DIR / "sprites" / "message.png": (184, 267),
        ASSETS_DIR / "sprites" / "gameover.png": (192, 42),
        ASSETS_DIR / "skins" / "classic.png": (34, 24),
        ASSETS_DIR / "skins" / "blue_bird.png": (34, 24),
        ASSETS_DIR / "skins" / "red_bird.png": (34, 24),
        ASSETS_DIR / "skins" / "custom_robin.png": (1023, 512),
    }

    for path, expected_size in expected_assets.items():
        assert path.exists(), f"Asset không tồn tại: {path}"
        with Image.open(path) as img:
            assert img.mode == "RGBA", f"Asset {path.name} mode={img.mode}, kỳ vọng RGBA"
            assert img.size == expected_size, f"Asset {path.name} size={img.size}, kỳ vọng {expected_size}"

    # Kiểm tra 10 chữ số retro 0-9
    digits_dir = ASSETS_DIR / "sprites" / "digits"
    assert digits_dir.is_dir(), f"Thư mục digits không tồn tại: {digits_dir}"
    for i in range(10):
        digit_path = digits_dir / f"{i}.png"
        assert digit_path.exists(), f"Thiếu sprite chữ số: {digit_path}"
        with Image.open(digit_path) as img:
            assert img.mode == "RGBA", f"Digit {i}.png mode={img.mode}, kỳ vọng RGBA"
            assert img.size[1] == 36, f"Digit {i}.png height={img.size[1]}, kỳ vọng 36px"
            if i == 1:
                assert img.size[0] == 16, f"Digit 1.png width={img.size[0]}, kỳ vọng 16px"
            else:
                assert img.size[0] == 24, f"Digit {i}.png width={img.size[0]}, kỳ vọng 24px"


def test_texture_filtering_is_nearest_neighbor():
    """Context default_atlas và SpriteList phải sử dụng bộ lọc GL_NEAREST để tránh nhòe pixel art."""
    import pyglet.gl as gl
    from src.main import FlappyWindow
    win = FlappyWindow(visible=False)
    assert win.ctx.default_atlas.texture.filter == (gl.GL_NEAREST, gl.GL_NEAREST)


def test_atlas_filter_persists_across_atlas_resize():
    """Bộ lọc GL_NEAREST phải bền vững ngay cả sau khi DefaultTextureAtlas auto-resize."""
    import pyglet.gl as gl
    from src.main import FlappyWindow
    win = FlappyWindow(visible=False)
    win.ctx.default_atlas.resize((1024, 1024), force=True)
    assert win.ctx.default_atlas.texture.filter == (gl.GL_NEAREST, gl.GL_NEAREST)

