"""Game constants cho Flappy Bird (Arcade 3.3.3)."""
import sys
from pathlib import Path

import pyglet
# Tắt DirectWrite/font antialiasing toàn cục để render pixel art font 100% sắc nét (1-bit binary alpha)
pyglet.options.text_antialiasing = False

# Root directory, assets và save data
if getattr(sys, "frozen", False):
    # Running trong PyInstaller executable (bundle temp chứa assets)
    PROJECT_ROOT = Path(sys._MEIPASS)
    # File save_data.json lưu cùng thư mục với .exe để persist save game
    USER_ROOT = Path(sys.executable).resolve().parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    USER_ROOT = PROJECT_ROOT

ASSETS_DIR = PROJECT_ROOT / "assets"
DATA_DIR = USER_ROOT / "data"
SAVE_FILE = DATA_DIR / "save_data.json"

# Virtual viewport dimensions
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
FLOOR_HEIGHT = 108.0          # Floor từ Y = 0 đến Y = 108
PLAYABLE_TOP = SCREEN_HEIGHT  # Y = 512
PLAYABLE_BOTTOM = FLOOR_HEIGHT # Y = 108
PLAYABLE_HEIGHT = PLAYABLE_TOP - PLAYABLE_BOTTOM # 404 px

# Fixed timestep cho physics loop
FIXED_DT = 1.0 / 60.0

# Physics config của Bird (Arcade: Y-up coordinate)
# Gốc Pygame: Flap -9 px/frame (30fps) -> Arcade: ~+270 px/s
FLAP_VELOCITY = 280.0
# Gốc Pygame: Acc +1 px/frame^2 (30fps) -> Arcade: ~-900 px/s^2
GRAVITY = -850.0
# Gốc Pygame: Max drop 10 px/frame (30fps) -> Arcade: ~-450 px/s
TERMINAL_VELOCITY = -450.0

# Bird rotation (degrees)
ROT_FLAP = 25.0               # Góc ngửa lên khi flap
ROT_VEL = -180.0              # Tốc độ nose-dive khi rơi (deg/s)
ROT_MIN = -90.0               # Max dive angle khi rơi
ROT_MAX = 25.0                # Max pitch-up angle

# Standard fixed hitbox dimensions của Bird (fixed)
STANDARD_HITBOX_WIDTH = 34.0
STANDARD_HITBOX_HEIGHT = 24.0

# Bird spawn position ban đầu
BIRD_START_X = int(SCREEN_WIDTH * 0.28)
BIRD_START_Y = int(FLOOR_HEIGHT + PLAYABLE_HEIGHT * 0.5)

# Pipe config
PIPE_WIDTH = 52.0
PIPE_HEIGHT = 320.0
PIPE_HORIZONTAL_SPACING = 175.0  # Min horizontal spacing giữa 2 pipe pairs

# Difficulty curve milestones
INITIAL_PIPE_SPEED = 180.0
MAX_PIPE_SPEED = 300.0
INITIAL_PIPE_GAP = 150.0
MIN_PIPE_GAP = 110.0
LERP_SPEED_FACTOR = 4.0          # Lerp speed factor theo delta_time

# Economy & achievements
SCORE_PER_COIN = 5               # Score to coins: 5 points = 1 coin

# Font Retro 8-bit Pixel Art & Safe Fallback
FONT_DIR = ASSETS_DIR / "fonts"
FONT_RETRO_PATH = FONT_DIR / "PressStart2P-Regular.ttf"
FONT_RETRO_NAME = "Press Start 2P"
FONT_RETRO_FAMILY = ("Press Start 2P", "Arial")


def ensure_retro_font_loaded() -> bool:
    """Load font Press Start 2P globally vào Arcade/Pyglet an toàn."""
    if FONT_RETRO_PATH.exists():
        try:
            import arcade
            arcade.load_font(FONT_RETRO_PATH)
            return True
        except Exception:
            return False
    return False
