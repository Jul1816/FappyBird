"""TrailManager quản lý trail catalog, unlock achievements và shop purchase/equip."""
from typing import Optional

from ..models.save_data import SaveData
from ..models.trail import DEFAULT_TRAILS, Trail


class TrailManager:
    def __init__(self, trails: Optional[list[Trail]] = None) -> None:
        self.trails: list[Trail] = trails or list(DEFAULT_TRAILS)

    def get_all_trails(self) -> list[Trail]:
        return list(self.trails)

    def get_trail(self, trail_id: str) -> Optional[Trail]:
        return next((t for t in self.trails if t.id == trail_id), None)

    def is_unlocked(self, trail: Trail, save_data: SaveData) -> bool:
        """Check trail đã unlock chưa (pure function, không mutate save_data)."""
        if trail.id in save_data.unlocked_trails:
            return True
        if trail.unlock_type == "default":
            return True
        if trail.unlock_type == "highscore" and save_data.high_score >= trail.unlock_value:
            return True
        if trail.unlock_type == "total_coins" and save_data.total_coins_collected >= trail.unlock_value:
            return True
        return False

    def check_achievements(self, save_data: SaveData) -> list[Trail]:
        """Check và unlock các trail đạt achievement milestones."""
        newly_unlocked: list[Trail] = []
        for trail in self.trails:
            if trail.id not in save_data.unlocked_trails and self.is_unlocked(trail, save_data):
                save_data.unlocked_trails.append(trail.id)
                newly_unlocked.append(trail)
        return newly_unlocked

    def can_buy(self, trail: Trail, save_data: SaveData) -> bool:
        """Check player có đủ coin để mua trail không."""
        if trail.id in save_data.unlocked_trails:
            return False
        if trail.unlock_type != "coin":
            return False
        return save_data.coins >= trail.price

    def buy_trail(self, trail_id: str, save_data: SaveData) -> bool:
        """Xử lý mua trail bằng coin."""
        trail = self.get_trail(trail_id)
        if not trail or not self.can_buy(trail, save_data):
            return False

        save_data.coins -= trail.price
        if trail_id not in save_data.unlocked_trails:
            save_data.unlocked_trails.append(trail_id)
        return True

    def equip_trail(self, trail_id: str, save_data: SaveData) -> bool:
        """Equip trail nếu đã unlocked."""
        trail = self.get_trail(trail_id)
        if not trail or not self.is_unlocked(trail, save_data):
            return False

        save_data.equipped_trail = trail_id
        return True
