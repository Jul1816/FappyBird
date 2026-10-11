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

    def to_dict(self) -> dict[str, Any]:
        return {
            "coins": max(0, int(self.coins)),
            "high_score": max(0, int(self.high_score)),
            "total_coins_collected": max(0, int(self.total_coins_collected)),
            "equipped_skin": str(self.equipped_skin),
            "unlocked_skins": list(set(self.unlocked_skins)),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SaveData":
        if not isinstance(data, dict):
            return cls()

        coins = max(0, int(data.get("coins", 0)))
        high_score = max(0, int(data.get("high_score", 0)))
        total_coins = max(0, int(data.get("total_coins_collected", 0)))
        equipped_skin = str(data.get("equipped_skin", "classic"))

        raw_unlocked = data.get("unlocked_skins", ["classic"])
        if not isinstance(raw_unlocked, list):
            raw_unlocked = ["classic"]
        unlocked_skins = [str(s) for s in raw_unlocked if isinstance(s, (str, int))]
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
