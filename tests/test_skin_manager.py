"""Unit tests for SkinManager service with new Duck and Phoenix catalog."""
import unittest

from src.models.save_data import SaveData
from src.services.skin_manager import SkinManager


class TestSkinManager(unittest.TestCase):
    def setUp(self):
        self.manager = SkinManager()
        self.save_data = SaveData(
            coins=20,
            high_score=15,
            total_coins_collected=20,
            equipped_skin="yellow",
            unlocked_skins=["yellow"],
        )

    def test_catalog_has_all_six_skins_in_order(self):
        skins = self.manager.get_all_skins()
        expected_ids = ["yellow", "electric", "cyber", "royal", "fiery", "custom_robin"]
        actual_ids = [s.id for s in skins]
        self.assertEqual(actual_ids, expected_ids)

    def test_default_skins_are_always_unlocked(self):
        yellow_skin = self.manager.get_skin("yellow")
        robin_skin = self.manager.get_skin("custom_robin")
        self.assertIsNotNone(yellow_skin)
        self.assertIsNotNone(robin_skin)
        self.assertTrue(self.manager.is_unlocked(yellow_skin, self.save_data))
        self.assertTrue(self.manager.is_unlocked(robin_skin, self.save_data))

    def test_can_buy_and_buy_electric_skin_success(self):
        # electric: price 10 coins, save_data có 20 coins
        electric_skin = self.manager.get_skin("electric")
        self.assertIsNotNone(electric_skin)
        self.assertTrue(self.manager.can_buy(electric_skin, self.save_data))

        # Thực hiện mua
        bought = self.manager.buy_skin("electric", self.save_data)
        self.assertTrue(bought)
        self.assertEqual(self.save_data.coins, 10)  # 20 - 10 = 10
        self.assertIn("electric", self.save_data.unlocked_skins)
        self.assertTrue(self.manager.is_unlocked(electric_skin, self.save_data))

    def test_cannot_buy_electric_when_insufficient_coins(self):
        self.save_data.coins = 5
        electric_skin = self.manager.get_skin("electric")
        self.assertIsNotNone(electric_skin)
        self.assertFalse(self.manager.can_buy(electric_skin, self.save_data))

        bought = self.manager.buy_skin("electric", self.save_data)
        self.assertFalse(bought)
        self.assertEqual(self.save_data.coins, 5)
        self.assertNotIn("electric", self.save_data.unlocked_skins)

    def test_achievement_auto_unlock_cyber_and_fiery_highscore(self):
        cyber_skin = self.manager.get_skin("cyber")
        fiery_skin = self.manager.get_skin("fiery")
        self.assertIsNotNone(cyber_skin)
        self.assertIsNotNone(fiery_skin)

        # Hiện tại highscore = 15 -> cả 2 chưa mở
        self.assertFalse(self.manager.is_unlocked(cyber_skin, self.save_data))
        self.assertFalse(self.manager.is_unlocked(fiery_skin, self.save_data))

        # Nâng highscore lên 25 -> cyber mở, fiery chưa mở (cần 50)
        self.save_data.high_score = 25
        newly_unlocked = self.manager.check_achievements(self.save_data)
        self.assertIn(cyber_skin, newly_unlocked)
        self.assertNotIn(fiery_skin, newly_unlocked)
        self.assertIn("cyber", self.save_data.unlocked_skins)
        self.assertNotIn("fiery", self.save_data.unlocked_skins)

        # Nâng highscore lên 50 -> fiery mở
        self.save_data.high_score = 50
        newly_unlocked_2 = self.manager.check_achievements(self.save_data)
        self.assertIn(fiery_skin, newly_unlocked_2)
        self.assertIn("fiery", self.save_data.unlocked_skins)

    def test_achievement_auto_unlock_royal_total_coins(self):
        royal_skin = self.manager.get_skin("royal")
        self.assertIsNotNone(royal_skin)

        # Hiện tại total_coins_collected = 20 -> chưa mở (cần 100)
        self.assertFalse(self.manager.is_unlocked(royal_skin, self.save_data))

        # Tích lũy đạt 100 coin -> mở khóa
        self.save_data.total_coins_collected = 100
        newly_unlocked = self.manager.check_achievements(self.save_data)
        self.assertIn(royal_skin, newly_unlocked)
        self.assertIn("royal", self.save_data.unlocked_skins)

    def test_equip_skin(self):
        # Không thể trang bị skin chưa mở
        equipped = self.manager.equip_skin("electric", self.save_data)
        self.assertFalse(equipped)
        self.assertEqual(self.save_data.equipped_skin, "yellow")

        # Có thể trang bị skin đã mở
        self.save_data.unlocked_skins.append("electric")
        equipped = self.manager.equip_skin("electric", self.save_data)
        self.assertTrue(equipped)
        self.assertEqual(self.save_data.equipped_skin, "electric")


if __name__ == "__main__":
    unittest.main()
