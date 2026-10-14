"""Comprehensive tests for new Duck & Phoenix skins: loading, auto-scaling, and hitbox invariance."""
import unittest
import arcade

from src.constants import ASSETS_DIR, STANDARD_HITBOX_HEIGHT, STANDARD_HITBOX_WIDTH
from src.entities.bird import Bird
from src.models.skin import DEFAULT_SKINS, Skin


class TestDuckSkins(unittest.TestCase):
    def test_all_skins_load_and_maintain_invariant_height_and_hitbox(self):
        hw = STANDARD_HITBOX_WIDTH / 2.0   # 17.0
        hh = STANDARD_HITBOX_HEIGHT / 2.0  # 12.0

        for skin in DEFAULT_SKINS:
            with self.subTest(skin_id=skin.id):
                tex = arcade.load_texture(skin.sprite_path)
                self.assertIsNotNone(tex, f"Failed to load texture for {skin.id}")

                bird = Bird(texture=tex, center_x=100.0, center_y=200.0)

                # Height on screen must strictly scale to 24.0 px
                expected_scale = 24.0 / float(tex.height)
                self.assertAlmostEqual(bird.scale[0], expected_scale, places=4)
                self.assertAlmostEqual(bird.scale[1], expected_scale, places=4)
                self.assertAlmostEqual(bird.height, 24.0, delta=0.01)

                # Hitbox must strictly be centered standard 34x24 px
                pts = bird.hit_box.points
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                self.assertAlmostEqual(min(xs), -hw, delta=0.01)
                self.assertAlmostEqual(max(xs), hw, delta=0.01)
                self.assertAlmostEqual(min(ys), -hh, delta=0.01)
                self.assertAlmostEqual(max(ys), hh, delta=0.01)

    def test_dynamic_skin_texture_update(self):
        bird = Bird()
        self.assertEqual(bird.scale, (1.0, 1.0))

        yellow_tex = arcade.load_texture(ASSETS_DIR / "skins" / "yellow.png")
        bird.set_skin_texture(yellow_tex)
        self.assertAlmostEqual(bird.height, 24.0, delta=0.01)

        fiery_tex = arcade.load_texture(ASSETS_DIR / "skins" / "fiery.png")
        bird.set_skin_texture(fiery_tex)
        self.assertAlmostEqual(bird.height, 24.0, delta=0.01)

        # Setting to None resets scale safely
        bird.set_skin_texture(None)
        self.assertEqual(bird.scale, (1.0, 1.0))


if __name__ == "__main__":
    unittest.main()
