"""Unit tests for ScoreDisplay: multi-digit retro score layout and bounding box centering."""
import pytest
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.entities.score_display import ScoreDisplay


def test_score_display_single_digit_centering():
    """1 chữ số (ví dụ: '0', '7') phải căn giữa hoàn hảo tại X = 144.0."""
    sd = ScoreDisplay()
    sd.set_score(0)
    assert len(sd.sprites) == 1
    sprite = sd.sprites[0]
    assert abs(sprite.center_x - 144.0) < 1e-3
    assert abs(sprite.center_y - (SCREEN_HEIGHT - 60.0)) < 1e-3


def test_score_display_multi_digit_bounding_box_centering():
    """Điểm số 2 chữ số (ví dụ: 14) có chiều rộng khác nhau (1: 16px, 4: 24px) phải có tâm Bounding Box = 144.0."""
    sd = ScoreDisplay()
    sd.set_score(14)
    assert len(sd.sprites) == 2

    # Tính tâm hình học Bounding Box
    min_left = min(s.left for s in sd.sprites)
    max_right = max(s.right for s in sd.sprites)
    bbox_center = (min_left + max_right) / 2.0

    assert abs(bbox_center - 144.0) < 1e-3
    # Tổng bề rộng = 16 + 24 = 40px -> left=124.0, right=164.0
    assert abs((max_right - min_left) - 40.0) < 1e-3
    assert abs(min_left - 124.0) < 1e-3
    assert abs(max_right - 164.0) < 1e-3


def test_score_display_three_digits_centering():
    """Điểm số 3 chữ số (ví dụ: 105) phải căn giữa Bounding Box tại X = 144.0."""
    sd = ScoreDisplay()
    sd.set_score(105)
    assert len(sd.sprites) == 3

    min_left = min(s.left for s in sd.sprites)
    max_right = max(s.right for s in sd.sprites)
    bbox_center = (min_left + max_right) / 2.0

    # 1: 16px, 0: 24px, 5: 24px -> Tổng bề rộng = 64px -> left=112.0, right=176.0
    assert abs(bbox_center - 144.0) < 1e-3
    assert abs((max_right - min_left) - 64.0) < 1e-3
    assert abs(min_left - 112.0) < 1e-3
    assert abs(max_right - 176.0) < 1e-3


def test_score_display_negative_score_clamped():
    """Điểm số âm được hiển thị an toàn như điểm 0."""
    sd = ScoreDisplay()
    sd.set_score(-5)
    assert len(sd.sprites) == 1
    assert abs(sd.sprites[0].center_x - 144.0) < 1e-3
