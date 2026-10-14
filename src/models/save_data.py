"""Model dữ liệu lưu trữ tiến trình người chơi."""
from dataclasses import dataclass, field
from typing import Any

VALID_SKIN_IDS = {"yellow", "electric", "cyber", "royal", "fiery", "custom_robin"}
DEPRECATED_SKIN_IDS = {"classic", "blue_bird", "red_bird", "cyber_bird", "golden_bird"}


@dataclass
class SaveData:
    coins: int = 0
    high_score: int = 0
    total_coins_collected: int = 0
    equipped_skin: str = "yellow"
    unlocked_skins: list[str] = field(default_factory=lambda: ["yellow"])

    @staticmethod
    def _safe_int(value: Any, default: int = 0) -> int:
        if isinstance(value, bool):
            return default
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def to_dict(self) -> dict[str, Any]:
        return {
            "coins": max(0, self._safe_int(self.coins, 0)),
            "high_score": max(0, self._safe_int(self.high_score, 0)),
            "total_coins_collected": max(0, self._safe_int(self.total_coins_collected, 0)),
            "equipped_skin": str(self.equipped_skin),
            "unlocked_skins": list(dict.fromkeys(self.unlocked_skins)),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SaveData":
        if not isinstance(data, dict):
            return cls()

        coins = max(0, cls._safe_int(data.get("coins", 0), 0))
        high_score = max(0, cls._safe_int(data.get("high_score", 0), 0))
        total_coins = max(0, cls._safe_int(data.get("total_coins_collected", 0), 0))
        equipped_skin = str(data.get("equipped_skin", "yellow") or "yellow")
        if equipped_skin in DEPRECATED_SKIN_IDS:
            equipped_skin = "yellow"

        raw_unlocked = data.get("unlocked_skins", ["yellow"])
        if not isinstance(raw_unlocked, list):
            raw_unlocked = ["yellow"]

        filtered_unlocked = []
        for s in raw_unlocked:
            if isinstance(s, (str, int)) and not isinstance(s, bool):
                s_str = str(s)
                if s_str not in DEPRECATED_SKIN_IDS and s_str in VALID_SKIN_IDS:
                    filtered_unlocked.append(s_str)

        unlocked_skins = list(dict.fromkeys(filtered_unlocked))
        if "yellow" not in unlocked_skins:
            unlocked_skins.insert(0, "yellow")

        if equipped_skin not in unlocked_skins:
            equipped_skin = "yellow"

        return cls(
            coins=coins,
            high_score=high_score,
            total_coins_collected=max(total_coins, coins),
            equipped_skin=equipped_skin,
            unlocked_skins=unlocked_skins,
        )
