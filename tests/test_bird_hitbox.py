"""Unit tests verifying Hitbox Invariance and physics for Bird entity."""
import unittest
from PIL import Image

import arcade
from src.constants import (
    FLAP_VELOCITY,
    GRAVITY,
    ROT_FLAP,
    ROT_MIN,
    STANDARD_HITBOX_HEIGHT,
    STANDARD_HITBOX_WIDTH,
    TERMINAL_VELOCITY,
)
from src.entities.bird import Bird


class TestBirdHitboxAndPhysics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Tạo 3 texture tạm thời với kích thước khác nhau: 32x32, 64x64, 100x50
        cls.temp_textures = {}
        for size in [(32, 32), (64, 64), (100, 50)]:
            img = Image.new("RGBA", size, (255, 200, 0, 255))
            cls.temp_textures[size] = arcade.Texture(img)

    def test_hitbox_invariance_across_different_texture_sizes(self):
        """Hitbox phải bất biến (34x24) với bất kỳ kích thước texture nào."""
        for size, texture in self.temp_textures.items():
            bird = Bird(texture=texture, center_x=100.0, center_y=200.0)

            # Hitbox points chưa xoay
            pts = bird.hit_box.points
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            width = max(xs) - min(xs)
            height = max(ys) - min(ys)

            self.assertEqual(
                width,
                STANDARD_HITBOX_WIDTH,
                f"Kích thước texture {size} tạo ra hitbox width = {width}, kỳ vọng {STANDARD_HITBOX_WIDTH}",
            )
            self.assertEqual(
                height,
                STANDARD_HITBOX_HEIGHT,
                f"Kích thước texture {size} tạo ra hitbox height = {height}, kỳ vọng {STANDARD_HITBOX_HEIGHT}",
            )

    def test_bird_flap_impulse(self):
        """Khi flap, vận tốc Y phải được gán bằng FLAP_VELOCITY và góc ngửa lên ROT_FLAP."""
        texture = self.temp_textures[(32, 32)]
        bird = Bird(texture=texture)
        bird.velocity_y = -300.0
        bird.angle = -60.0

        bird.flap()
        self.assertEqual(bird.velocity_y, FLAP_VELOCITY)
        self.assertEqual(bird.angle, ROT_FLAP)

    def test_bird_gravity_and_terminal_velocity(self):
        """Rơi tự do phải chịu gia tốc GRAVITY và không được vượt quá TERMINAL_VELOCITY."""
        texture = self.temp_textures[(32, 32)]
        bird = Bird(texture=texture, center_x=100.0, center_y=300.0)
        bird.velocity_y = 0.0

        # Cập nhật 1 giây rơi tự do
        for _ in range(60):
            bird.update_physics(1.0 / 60.0)

        # Vận tốc không được nhỏ hơn TERMINAL_VELOCITY (ví dụ -450)
        self.assertGreaterEqual(bird.velocity_y, TERMINAL_VELOCITY)
        self.assertEqual(bird.velocity_y, TERMINAL_VELOCITY)

    def test_bird_downward_rotation_clamps_at_rot_min(self):
        """Khi rơi lâu, góc chúc đầu của chim phải giảm dần và khóa ở ROT_MIN (-90 độ)."""
        texture = self.temp_textures[(32, 32)]
        bird = Bird(texture=texture, center_x=100.0, center_y=300.0)
        bird.flap()
        for _ in range(120):
            bird.update_physics(1.0 / 60.0)
        self.assertEqual(bird.angle, ROT_MIN)
        self.assertFalse(hasattr(bird, "attachments"))
        self.assertFalse(hasattr(bird, "trail_enabled"))

    def test_bird_auto_fit_scale_matches_hitbox_height(self):
        """Chiều cao hiển thị của chim phải luôn tự động co giãn bằng đúng chiều cao hitbox (24.0 px)."""
        # 1. Texture Robin khổng lồ 1023x512
        im_robin = Image.new("RGBA", (1023, 512), (255, 255, 255, 255))
        tex_robin = arcade.Texture(im_robin)
        bird = Bird(texture=tex_robin)

        self.assertAlmostEqual(bird.height, STANDARD_HITBOX_HEIGHT, delta=1e-3)
        self.assertAlmostEqual(bird.scale[1], 24.0 / 512.0, delta=1e-5)
        # Chiều rộng hiển thị tỷ lệ thuận: 1023 * (24/512) ≈ 47.95 px
        self.assertAlmostEqual(bird.width, 1023.0 * (24.0 / 512.0), delta=1e-2)

        # Hitbox bất biến: rộng 34, cao 24
        pts = bird.hit_box.points
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        self.assertEqual(max(xs) - min(xs), STANDARD_HITBOX_WIDTH)
        self.assertEqual(max(ys) - min(ys), STANDARD_HITBOX_HEIGHT)

    def test_bird_none_texture_and_set_skin_texture_safety(self):
        """Khởi tạo chim với texture=None phải an toàn và set_skin_texture cập nhật scale đúng."""
        bird = Bird(texture=None)
        self.assertEqual(bird.scale, (1.0, 1.0))

        # Cập nhật skin động qua set_skin_texture
        im_classic = Image.new("RGBA", (34, 24), (255, 200, 0, 255))
        tex_classic = arcade.Texture(im_classic)
        bird.set_skin_texture(tex_classic)
        self.assertAlmostEqual(bird.scale[1], 1.0, delta=1e-4)
        self.assertAlmostEqual(bird.height, 24.0, delta=1e-3)


if __name__ == "__main__":
    unittest.main()

