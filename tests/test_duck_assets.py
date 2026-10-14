"""Unit tests verifying the presence and format of new duck and phoenix skin assets."""
from pathlib import Path
import unittest
from PIL import Image

from src.constants import ASSETS_DIR


class TestDuckAssets(unittest.TestCase):
    def test_all_duck_and_phoenix_textures_exist_and_are_rgba(self):
        skins_dir = ASSETS_DIR / "skins"
        expected_skins = {
            "yellow.png": (94, 56),
            "electric.png": (47, 30),
            "cyber.png": (44, 26),
            "royal.png": (47, 32),
            "fiery.png": (98, 65),
            "custom_robin.png": (1023, 512),
        }

        for filename, expected_size in expected_skins.items():
            path = skins_dir / filename
            self.assertTrue(path.exists(), f"Skin texture missing: {filename}")
            with Image.open(path) as img:
                self.assertEqual(img.mode, "RGBA", f"Skin {filename} mode is {img.mode}, expected RGBA")
                self.assertEqual(img.size, expected_size, f"Skin {filename} size is {img.size}, expected {expected_size}")


if __name__ == "__main__":
    unittest.main()
