"""Unit tests for StorageService with new duck skins and legacy migration."""
import tempfile
import unittest
from pathlib import Path

from src.models.save_data import SaveData
from src.services.storage import StorageService


class TestStorageService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.save_file = Path(self.temp_dir.name) / "save_data.json"
        self.service = StorageService(save_path=self.save_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_non_existent_file_returns_default(self):
        data = self.service.load()
        self.assertIsInstance(data, SaveData)
        self.assertEqual(data.coins, 0)
        self.assertEqual(data.high_score, 0)
        self.assertEqual(data.equipped_skin, "yellow")
        self.assertEqual(data.unlocked_skins, ["yellow"])

    def test_save_and_load_round_trip(self):
        save_data = SaveData(
            coins=35,
            high_score=78,
            total_coins_collected=50,
            equipped_skin="electric",
            unlocked_skins=["yellow", "electric"],
        )
        saved = self.service.save(save_data)
        self.assertTrue(saved)
        self.assertTrue(self.save_file.exists())

        loaded = self.service.load()
        self.assertEqual(loaded.coins, 35)
        self.assertEqual(loaded.high_score, 78)
        self.assertEqual(loaded.total_coins_collected, 50)
        self.assertEqual(loaded.equipped_skin, "electric")
        self.assertIn("yellow", loaded.unlocked_skins)
        self.assertIn("electric", loaded.unlocked_skins)

    def test_corrupted_json_recovery(self):
        self.save_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.save_file, "w", encoding="utf-8") as f:
            f.write("INVALID JSON CONTENT {{{ 1234")

        loaded = self.service.load()
        self.assertIsInstance(loaded, SaveData)
        self.assertEqual(loaded.coins, 0)
        self.assertEqual(loaded.high_score, 0)
        self.assertEqual(loaded.equipped_skin, "yellow")
        self.assertEqual(loaded.unlocked_skins, ["yellow"])

    def test_atomic_write_leaves_no_tmp_file(self):
        save_data = SaveData(coins=10, high_score=15)
        self.service.save(save_data)
        tmp_files = list(self.save_file.parent.glob("*.tmp"))
        self.assertEqual(len(tmp_files), 0)

    def test_legacy_skins_are_filtered_and_fallback_to_yellow(self):
        self.save_file.parent.mkdir(parents=True, exist_ok=True)
        self.save_file.write_text(
            '{"coins": 45, "high_score": 30, "total_coins_collected": 50, "equipped_skin": "classic", "unlocked_skins": ["classic", "blue_bird", "red_bird", "cyber_bird", "golden_bird"]}',
            encoding="utf-8",
        )
        loaded = self.service.load()
        self.assertEqual(loaded.coins, 45)
        self.assertEqual(loaded.high_score, 30)
        self.assertEqual(loaded.total_coins_collected, 50)
        self.assertEqual(loaded.equipped_skin, "yellow")
        self.assertEqual(loaded.unlocked_skins, ["yellow"])

    def test_custom_robin_is_preserved_during_legacy_migration(self):
        self.save_file.parent.mkdir(parents=True, exist_ok=True)
        self.save_file.write_text(
            '{"coins": 10, "high_score": 10, "total_coins_collected": 10, "equipped_skin": "custom_robin", "unlocked_skins": ["classic", "blue_bird", "custom_robin"]}',
            encoding="utf-8",
        )
        loaded = self.service.load()
        self.assertEqual(loaded.equipped_skin, "custom_robin")
        self.assertIn("custom_robin", loaded.unlocked_skins)
        self.assertIn("yellow", loaded.unlocked_skins)
        self.assertNotIn("classic", loaded.unlocked_skins)
        self.assertNotIn("blue_bird", loaded.unlocked_skins)

    def test_utf8_bom_file_loads_correctly(self):
        self.save_file.parent.mkdir(parents=True, exist_ok=True)
        bom_content = '\ufeff{"coins": 42, "high_score": 99, "total_coins_collected": 100, "equipped_skin": "yellow", "unlocked_skins": ["yellow"]}'
        self.save_file.write_text(bom_content, encoding="utf-8")

        loaded = self.service.load()
        self.assertEqual(loaded.coins, 42)
        self.assertEqual(loaded.high_score, 99)
        self.assertEqual(loaded.total_coins_collected, 100)
        self.assertEqual(loaded.equipped_skin, "yellow")


if __name__ == "__main__":
    unittest.main()
