# Implementation Plan: Duck & Phoenix Skins

## Overview
Kế hoạch triển khai thay thế toàn bộ hệ thống skins và texture chim cũ (trừ Angel Robin `custom_robin`) bằng 5 texture mới từ `C:\Users\Admin\Desktop\ducks\trimmed`, cập nhật cơ chế mở khóa và reset SaveData an toàn.
Chi tiết xem tại [2026-10-14-duck-and-phoenix-skins.md](file:///e:/FlappyBird/docs/superpowers/plans/2026-10-14-duck-and-phoenix-skins.md).

---

## Architecture Decisions
1. **Chuẩn hóa Texture sang RGBA & Quản lý File An Toàn**:
   - Sao chép 5 texture mới từ `C:\Users\Admin\Desktop\ducks\trimmed` sang `assets/skins/` với tên chuẩn hóa theo ID: `yellow.png` (94x56), `electric.png` (47x30), `cyber.png` (44x26), `royal.png` (47x32), `fiery.png` (98x65).
   - Bảo toàn 100% file `custom_robin.png` (1023x512) và giữ các file cũ làm backup.
2. **Cập nhật Danh mục `DEFAULT_SKINS`**:
   - `yellow`: Yellow Duck (default, price 0)
   - `electric`: Lightning Blue (coin, price 10)
   - `cyber`: Cybernetic (highscore, req 25)
   - `royal`: Royal Gold (total_coins, req 100)
   - `fiery`: Fiery Phoenix (highscore, req 50)
   - `custom_robin`: Angel Robin (default, price 0)
3. **Cơ chế Sanitization và Fallback cho SaveData**:
   - Mặc định `equipped_skin = "yellow"`, `unlocked_skins = ["yellow"]`.
   - Trong `SaveData.from_dict`: Khử khuẩn các ID skin cũ (`classic`, `blue_bird`, `red_bird`, `cyber_bird`, `golden_bird`). Bảo lưu `custom_robin` nếu đã có. Fallback `equipped_skin` về `"yellow"` nếu đang dùng skin cũ.
4. **Hitbox & Dynamic Scaling**:
   - Thực thể `Bird` tự động gán `scale = 24.0 / texture.height` đảm bảo mọi skin có chiều cao hiển thị $24.0\text{ px}$.
   - Hitbox bất biến $34 \times 24\text{ px}$ căn giữa tâm chim.

---

## Tasks Summary & Checkpoints

### Phase 1: Asset Pipeline & Sprite Migration
- **Task 1**: Asset Pipeline & Sprite Migration (`src/tools/import_duck_assets.py`, `tests/test_duck_assets.py`)
- **Checkpoint 1**: 5 file texture mới có mặt trong `assets/skins/` chuẩn RGBA.

### Phase 2: Models & Storage Migration
- **Task 2**: Skin Catalog & Model Configuration (`src/models/skin.py`, `tests/test_skin_manager.py`)
- **Task 3**: SaveData Backward Compatibility & Reset Logic (`src/models/save_data.py`, `tests/test_storage.py`)
- **Checkpoint 2**: SkinManager và SaveData hoạt động hoàn hảo với 6 skin mới và tự động sanitize save data cũ.

### Phase 3: Views, Hitbox Integrity & Full Regression
- **Task 4**: View Integration & Fallback Updates (`src/views/shop_view.py`, `src/main.py`, `tests/test_e2e_views.py`)
- **Task 5**: Hitbox Integrity, Crisp Rendering & Full Regression (`tests/test_crisp_rendering.py`, `tests/test_duck_skins.py`)
- **Checkpoint 3**: Hoàn thành toàn bộ, 100% test suite `python -m pytest` pass.
