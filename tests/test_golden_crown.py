"""Tests for Golden Bird crown placement, eye integrity, and hitbox alignment."""
from pathlib import Path
import unittest
from PIL import Image
import numpy as np
import arcade

from src.constants import ASSETS_DIR
from src.entities.bird import Bird


class TestGoldenBirdCrown(unittest.TestCase):
    def setUp(self) -> None:
        self.golden_path = ASSETS_DIR / "skins" / "golden_bird.png"
        self.assertTrue(self.golden_path.exists(), "golden_bird.png must exist")

    def test_golden_bird_dimensions_and_rgba(self) -> None:
        with Image.open(self.golden_path) as img:
            self.assertEqual(img.size, (34, 24), "Golden bird must preserve authentic 34x24 dimensions")
            self.assertEqual(img.mode, "RGBA", "Golden bird must be in RGBA format")

    def test_golden_crown_pixels_and_eye_integrity(self) -> None:
        with Image.open(self.golden_path) as img:
            arr = np.array(img)

        # 1. Crown peaks at row y=0
        peak_center = arr[0, 16]
        self.assertGreater(peak_center[0], 200, "Crown center peak must be bright gold")
        self.assertGreater(peak_center[1], 200, "Crown center peak must be bright gold")
        self.assertEqual(peak_center[3], 255, "Crown peak must be opaque")

        # 2. Ruby jewel at (16, 1)
        ruby = arr[1, 16]
        self.assertGreater(ruby[0], 200, "Ruby must have high red channel")
        self.assertLess(ruby[1], 60, "Ruby must have low green channel")
        self.assertLess(ruby[2], 60, "Ruby must have low blue channel")

        # 3. Eye white at (21, 2) and (21, 3) must be untouched (> 240 in all RGB channels)
        eye_white_1 = arr[2, 21]
        eye_white_2 = arr[3, 21]
        self.assertTrue((eye_white_1[:3] > 240).all(), f"Eye white at (21, 2) must be preserved: {eye_white_1}")
        self.assertTrue((eye_white_2[:3] > 240).all(), f"Eye white at (21, 3) must be preserved: {eye_white_2}")

        # 4. Pupil at (24, 7) must remain dark outline/pupil color [83, 56, 70]
        pupil = arr[7, 24]
        self.assertEqual(pupil[3], 255)
        self.assertLess(pupil[0], 100, "Pupil must remain dark")

    def test_golden_bird_entity_hitbox_and_scale(self) -> None:
        tex = arcade.load_texture(self.golden_path)
        bird = Bird(texture=tex, center_x=100.0, center_y=200.0)

        # Scale must be exactly 1.0 (24.0 / 24.0)
        self.assertEqual(bird.scale, (1.0, 1.0))
        self.assertAlmostEqual(bird.height, 24.0, delta=0.01)
        self.assertAlmostEqual(bird.width, 34.0, delta=0.01)

        # Hitbox must be exactly 34x24 centered at (0, 0)
        pts = bird.hit_box.points
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.assertEqual(min(xs), -17.0)
        self.assertEqual(max(xs), 17.0)
        self.assertEqual(min(ys), -12.0)
        self.assertEqual(max(ys), 12.0)


if __name__ == "__main__":
    unittest.main()
