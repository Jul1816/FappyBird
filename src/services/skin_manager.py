"""SkinManager quản lý skin catalog, unlock achievements và shop purchase/equip."""
from typing import Optional

from ..models.save_data import SaveData
from ..models.skin import DEFAULT_SKINS, Skin


class SkinManager:
    def __init__(self, skins: Optional[list[Skin]] = None) -> None:
        self.skins: list[Skin] = skins or list(DEFAULT_SKINS)

    def get_all_skins(self) -> list[Skin]:
        return list(self.skins)

    def get_skin(self, skin_id: str) -> Optional[Skin]:
        return next((s for s in self.skins if s.id == skin_id), None)

    def is_unlocked(self, skin: Skin, save_data: SaveData) -> bool:
        """Check skin đã unlock chưa (pure function, không mutate save_data)."""
        if skin.id in save_data.unlocked_skins:
            return True
        if skin.unlock_type == "default":
            return True
        if skin.unlock_type == "highscore" and save_data.high_score >= skin.unlock_value:
            return True
        if skin.unlock_type == "total_coins" and save_data.total_coins_collected >= skin.unlock_value:
            return True
        return False

    def check_achievements(self, save_data: SaveData) -> list[Skin]:
        """Check và unlock các skin đạt achievement milestones."""
        newly_unlocked: list[Skin] = []
        for skin in self.skins:
            if skin.id not in save_data.unlocked_skins and self.is_unlocked(skin, save_data):
                save_data.unlocked_skins.append(skin.id)
                newly_unlocked.append(skin)
        return newly_unlocked

    def can_buy(self, skin: Skin, save_data: SaveData) -> bool:
        """Check player có đủ coin để mua skin không."""
        if skin.id in save_data.unlocked_skins:
            return False
        if skin.unlock_type != "coin":
            return False
        return save_data.coins >= skin.price

    def buy_skin(self, skin_id: str, save_data: SaveData) -> bool:
        """Xử lý mua skin bằng coin."""
        skin = self.get_skin(skin_id)
        if not skin or not self.can_buy(skin, save_data):
            return False

        save_data.coins -= skin.price
        if skin_id not in save_data.unlocked_skins:
            save_data.unlocked_skins.append(skin_id)
        return True

    def equip_skin(self, skin_id: str, save_data: SaveData) -> bool:
        """Equip skin nếu đã unlocked."""
        skin = self.get_skin(skin_id)
        if not skin or not self.is_unlocked(skin, save_data):
            return False

        save_data.equipped_skin = skin_id
        return True
