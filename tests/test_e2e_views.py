"""Integration & E2E Tests: Window lifecycle, view transitions, input & rendering."""
from pathlib import Path
import tempfile
import unittest
import arcade

from src.main import FlappyWindow
from src.services.storage import StorageService
from src.views.start_view import StartView
from src.views.game_view import GameView
from src.views.game_over_view import GameOverView
from src.views.shop_view import ShopView


class TestE2EViews(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.temp_save_file = Path(cls.temp_dir.name) / "save_data.json"
        cls.window = FlappyWindow(
            storage=StorageService(save_path=cls.temp_save_file),
            visible=False,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.window.close()
        cls.temp_dir.cleanup()

    def setUp(self) -> None:
        # Reset save data to clean state in memory
        self.window.save_data.coins = 50
        self.window.save_data.high_score = 10
        self.window.save_data.total_coins_collected = 50
        self.window.save_data.equipped_skin = "yellow"
        self.window.save_data.unlocked_skins = ["yellow"]
        self.window.reload_skin_texture()

    def test_start_view_render_and_transition(self) -> None:
        start_view = StartView()
        self.window.show_view(start_view)
        start_view.on_update(1 / 60.0)
        start_view.on_draw()

        self.assertIsNotNone(start_view.bird)
        self.assertEqual(len(start_view.bird_list), 1)

        # Space starts game
        start_view.on_key_press(arcade.key.SPACE, 0)
        self.assertIsInstance(self.window.current_view, GameView)

    def test_start_view_to_shop_transition(self) -> None:
        start_view = StartView()
        self.window.show_view(start_view)
        # 'S' opens shop
        start_view.on_key_press(arcade.key.S, 0)
        self.assertIsInstance(self.window.current_view, ShopView)

    def test_shop_view_navigation_and_purchase(self) -> None:
        shop_view = ShopView(return_view="start")
        self.window.show_view(shop_view)
        shop_view.on_update(1 / 60.0)
        shop_view.on_draw()

        # Navigate skins
        initial_idx = shop_view.selected_index
        shop_view.next_skin()
        self.assertEqual(shop_view.selected_index, (initial_idx + 1) % len(shop_view.skins))

        # Select a skin that can be bought
        target_skin = None
        for i, s in enumerate(shop_view.skins):
            if s.unlock_type == "coin" and s.price <= self.window.save_data.coins:
                shop_view.selected_index = i
                target_skin = s
                break

        if target_skin:
            initial_coins = self.window.save_data.coins
            shop_view.perform_action()  # Buy and equip
            self.assertIn(target_skin.id, self.window.save_data.unlocked_skins)
            self.assertEqual(self.window.save_data.equipped_skin, target_skin.id)
            self.assertEqual(self.window.save_data.coins, initial_coins - target_skin.price)

        # Back to start
        shop_view.on_key_press(arcade.key.ESCAPE, 0)
        self.assertIsInstance(self.window.current_view, StartView)

    def test_game_view_loop_and_debug_keys(self) -> None:
        game_view = GameView()
        self.window.show_view(game_view)
        game_view.on_update(1 / 60.0)
        game_view.on_draw()

        self.assertEqual(game_view.score, 0)

        # Test debug hotkeys
        # F1: +10 coins
        c_before = self.window.save_data.coins
        game_view.on_key_press(arcade.key.F1, 0)
        self.assertEqual(self.window.save_data.coins, c_before + 10)

        # F2: Toggle hitbox
        hb_before = self.window.debug_hitbox
        game_view.on_key_press(arcade.key.F2, 0)
        self.assertEqual(self.window.debug_hitbox, not hb_before)

        # F3: +10 Score & coins
        s_before = game_view.score
        game_view.on_key_press(arcade.key.F3, 0)
        self.assertEqual(game_view.score, s_before + 10)

        # F4: God mode
        gm_before = self.window.god_mode
        game_view.on_key_press(arcade.key.F4, 0)
        self.assertEqual(self.window.god_mode, not gm_before)

        # Trigger die
        game_view.die("floor")
        self.assertTrue(game_view.is_dead)
        game_view.trigger_game_over()
        self.assertIsInstance(self.window.current_view, GameOverView)

    def test_game_over_view_replay(self) -> None:
        game_over = GameOverView(score=25, coins_earned=5)
        self.window.show_view(game_over)
        game_over.on_update(1 / 60.0)
        game_over.on_draw()

        # Space restarts game
        game_over.on_key_press(arcade.key.SPACE, 0)
        self.assertIsInstance(self.window.current_view, GameView)

    def test_game_over_to_shop_and_back_preserves_score_and_coins(self) -> None:
        game_over = GameOverView(score=35, coins_earned=7)
        self.window.show_view(game_over)
        game_over.on_key_press(arcade.key.S, 0)
        self.assertIsInstance(self.window.current_view, ShopView)

        # Press ESC in ShopView to return to GameOverView
        self.window.current_view.on_key_press(arcade.key.ESCAPE, 0)
        self.assertIsInstance(self.window.current_view, GameOverView)
        restored: GameOverView = self.window.current_view  # type: ignore
        self.assertEqual(restored.score, 35)
        self.assertEqual(restored.coins_earned, 7)
        self.assertEqual(restored.score_text.text, "SCORE: 35")

    def test_die_auto_unlocks_achievement_skins_and_isolates_save_file(self) -> None:
        game_view = GameView()
        self.window.show_view(game_view)
        game_view.score = 25
        game_view.die("pipe")
        self.assertIn("cyber", self.window.save_data.unlocked_skins)
        self.assertTrue(self.temp_save_file.exists())


if __name__ == "__main__":
    unittest.main()
