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
        ASSETS_DIR / "skins" / "yellow.png": (94, 56),
        ASSETS_DIR / "skins" / "electric.png": (47, 30),
        ASSETS_DIR / "skins" / "cyber.png": (44, 26),
        ASSETS_DIR / "skins" / "royal.png": (47, 32),
        ASSETS_DIR / "skins" / "fiery.png": (98, 65),
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


def test_message_sprite_grey_bird_erased():
    """Icon chim màu xám trong message.png phải được xóa hoàn toàn (alpha = 0 tại rows 168..202, cols 68..112)."""
    import numpy as np
    message_path = ASSETS_DIR / "sprites" / "message.png"
    assert message_path.exists(), "message.png must exist"
    with Image.open(message_path) as img:
        arr = np.array(img)
    grey_bird_region = arr[168:202, 68:112, 3]
    assert (grey_bird_region > 0).sum() == 0, "Icon chim màu xám chưa được xóa khỏi message.png"


def test_pyglet_text_antialiasing_is_disabled():
    """Tùy chọn pyglet text_antialiasing phải là False để bảo đảm font 1-bit không bị mờ nhòe."""
    import pyglet
    assert pyglet.options.text_antialiasing is False


def test_start_view_bird_centered_at_tutorial_position():
    """Chim trong StartView phải xuất hiện và lắc lư ngay tại vị trí trung tâm (X=142.0, Y=259.0)."""
    from src.main import FlappyWindow
    from src.views.start_view import StartView
    win = FlappyWindow(visible=False)
    start_view = StartView()
    win.show_view(start_view)

    assert start_view.bird is not None
    assert start_view.bird.center_x == 142.0
    assert start_view.bird.center_y == 259.0

    # Lắc lư qua 1 frame vẫn bảo toàn trục X=142.0 và dao động điều hòa quanh Y=259.0
    start_view.on_update(0.1)
    assert start_view.bird.center_x == 142.0
    assert abs(start_view.bird.center_y - 259.0) <= 7.0


def test_ui_boxes_fit_text_without_overflow():
    """Các nút bấm trong GameOverView, ShopView, StartView phải rộng hơn độ dài chữ bên trong (không bị tràn box)."""
    from src.main import FlappyWindow
    from src.views.game_over_view import GameOverView
    from src.views.shop_view import ShopView
    from src.views.start_view import StartView

    win = FlappyWindow(visible=False)

    # 1. GameOverView: btn_replay và btn_shop
    gov = GameOverView(score=25, coins_earned=5)
    win.show_view(gov)
    replay_w = gov.btn_replay[1] - gov.btn_replay[0]
    shop_w = gov.btn_shop[1] - gov.btn_shop[0]
    assert replay_w >= gov.replay_btn_text.content_width + 16.0, f"btn_replay ({replay_w}px) tràn chữ ({gov.replay_btn_text.content_width}px)"
    assert shop_w >= gov.shop_btn_text.content_width + 16.0, f"btn_shop ({shop_w}px) tràn chữ ({gov.shop_btn_text.content_width}px)"

    # 2. ShopView: btn_back và btn_action
    sv = ShopView()
    win.show_view(sv)
    back_w = sv.btn_back[1] - sv.btn_back[0]
    action_w = sv.btn_action[1] - sv.btn_action[0]
    assert back_w >= sv.back_btn_text.content_width + 16.0, f"btn_back ({back_w}px) tràn chữ ({sv.back_btn_text.content_width}px)"
    assert action_w >= sv.action_btn_text.content_width + 16.0, f"btn_action ({action_w}px) tràn chữ ({sv.action_btn_text.content_width}px)"

    # 3. StartView: shop_button_bounds
    start_view = StartView()
    win.show_view(start_view)
    start_shop_w = start_view.shop_button_bounds[1] - start_view.shop_button_bounds[0]
    assert start_shop_w >= start_view.shop_btn_text.content_width + 16.0, f"start shop btn ({start_shop_w}px) tràn chữ ({start_view.shop_btn_text.content_width}px)"


