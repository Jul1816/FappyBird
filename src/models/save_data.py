"""Model dữ liệu lưu trữ tiến trình người chơi."""
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SaveData:
    coins: int = 0
    high_score: int = 0
    total_coins_collected: int = 0
    equipped_skin: str = "classic"
    unlocked_skins: list[str] = field(default_factory=lambda: ["classic"])

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
        equipped_skin = str(data.get("equipped_skin", "classic") or "classic")

        raw_unlocked = data.get("unlocked_skins", ["classic"])
        if not isinstance(raw_unlocked, list):
            raw_unlocked = ["classic"]
        unlocked_skins = list(
            dict.fromkeys(str(s) for s in raw_unlocked if isinstance(s, (str, int)) and not isinstance(s, bool))
        )
        if "classic" not in unlocked_skins:
            unlocked_skins.insert(0, "classic")

        if equipped_skin not in unlocked_skins:
            equipped_skin = "classic"

        return cls(
            coins=coins,
            high_score=high_score,
            total_coins_collected=max(total_coins, coins),
            equipped_skin=equipped_skin,
            unlocked_skins=unlocked_skins,
        )
