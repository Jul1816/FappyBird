# Task List: Duck & Phoenix Skins

## Phase 1: Asset Pipeline & Sprite Migration

- [x] Task 1: Asset Pipeline & Sprite Migration
  - **Description:** Xây dựng script `src/tools/import_duck_assets.py` để copy 5 texture từ `C:\Users\Admin\Desktop\ducks\trimmed` sang `assets/skins/` (`yellow.png`, `electric.png`, `cyber.png`, `royal.png`, `fiery.png`) chuẩn định dạng RGBA. Bảo lưu `custom_robin.png` và các file cũ.
  - **Acceptance criteria:**
    - 5 file texture mới có mặt trong `assets/skins/` với định dạng RGBA.
    - Kích thước ảnh khớp với nguồn trên Desktop.
    - `custom_robin.png` được bảo toàn nguyên vẹn.
  - **Verification:** `python -m pytest tests/test_duck_assets.py`.
  - **Dependencies:** None
  - **Files likely touched:** `src/tools/import_duck_assets.py`, `tests/test_duck_assets.py`, `assets/skins/*.png`
  - **Estimated scope:** S (2 files + assets)

### Checkpoint 1: Asset Foundation
- [x] 5 texture mới đã có mặt tại `assets/skins/` và vượt qua bài test format RGBA.

---

## Phase 2: Models & Storage Migration

- [x] Task 2: Skin Catalog & Model Configuration
  - **Description:** Cập nhật `DEFAULT_SKINS` trong `src/models/skin.py` sang danh mục 6 skin mới: `yellow` (default), `electric` (10 coins), `cyber` (highscore 25), `royal` (total_coins 100), `fiery` (highscore 50), `custom_robin` (default). Cập nhật mô tả retro tiếng Anh.
  - **Acceptance criteria:**
    - `DEFAULT_SKINS` chứa đúng 6 skin theo thứ tự.
    - `SkinManager.is_unlocked`, `can_buy`, `check_achievements` nhận diện chính xác các mốc unlock mới.
  - **Verification:** `python -m pytest tests/test_skin_manager.py`.
  - **Dependencies:** Task 1
  - **Files likely touched:** `src/models/skin.py`, `tests/test_skin_manager.py`
  - **Estimated scope:** S (2 files)

- [x] Task 3: SaveData Backward Compatibility & Reset Logic
  - **Description:** Cập nhật `SaveData` trong `src/models/save_data.py`: default `equipped_skin="yellow"`, default `unlocked_skins=["yellow"]`. Trong `from_dict`: loại bỏ các ID cũ (`classic`, `blue_bird`, `red_bird`, `cyber_bird`, `golden_bird`), bảo lưu `custom_robin` nếu có, fallback `equipped_skin` về `yellow` nếu skin cũ.
  - **Acceptance criteria:**
    - Nạp file save cũ tự động lọc bỏ skin cũ, chỉ còn `yellow` (và `custom_robin` nếu đã có).
    - `equipped_skin` trỏ vào skin cũ tự động fallback về `yellow`.
    - Trạng thái lưu mới giữ nguyên tính toàn vẹn.
  - **Verification:** `python -m pytest tests/test_storage.py`.
  - **Dependencies:** Task 2
  - **Files likely touched:** `src/models/save_data.py`, `tests/test_storage.py`
  - **Estimated scope:** S (2 files)

### Checkpoint 2: Data & Business Logic Ready
- [x] Models và SaveData đã đồng bộ hoàn toàn với danh mục skin mới.
- [x] Các bài test logic nghiệp vụ `test_skin_manager.py` và `test_storage.py` pass 100%.

---

## Phase 3: Views, Hitbox Integrity & Full Regression

- [x] Task 4: View Integration & Fallback Updates
  - **Description:** Cập nhật fallback texture trong `src/views/shop_view.py` và `src/main.py` từ `classic.png` sang `yellow.png`. Đảm bảo `ShopView` duyệt đủ 6 skin và hiển thị preview mượt mà.
  - **Acceptance criteria:**
    - `ShopView` hiển thị đúng 6 skin theo thứ tự định sẵn.
    - Không crash nếu thiếu texture (fallback sang `yellow.png`).
    - Nút mua/trang bị hoạt động trơn tru.
  - **Verification:** `python -m pytest tests/test_e2e_views.py`.
  - **Dependencies:** Task 2, Task 3
  - **Files likely touched:** `src/views/shop_view.py`, `src/main.py`, `tests/test_e2e_views.py`
  - **Estimated scope:** S (3 files)

- [x] Task 5: Hitbox Integrity, Crisp Rendering & Full Regression
  - **Description:** Cập nhật `tests/test_crisp_rendering.py` cho 5 texture mới, thay thế `tests/test_golden_crown.py` bằng `tests/test_duck_skins.py` để kiểm tra auto-scaling `height == 24.0 px` và hitbox chuẩn $34 \times 24\text{ px}$ cho mọi skin. Chạy full regression test suite.
  - **Acceptance criteria:**
    - Toàn bộ 6 skin khi đưa vào thực thể `Bird` đều có `bird.height == 24.0 px` và hitbox $34 \times 24\text{ px}$.
    - Toàn bộ test suite chạy `python -m pytest` đạt 100% Passed (không có lỗi hay hồi quy).
  - **Verification:** `python -m pytest -v`.
  - **Dependencies:** Task 1, Task 2, Task 3, Task 4
  - **Files likely touched:** `tests/test_crisp_rendering.py`, `tests/test_duck_skins.py`, `tests/test_golden_crown.py`
  - **Estimated scope:** M (3 files)

### Checkpoint 3: Complete & Production Ready
- [x] Cả 5 tasks hoàn thành với verification rõ ràng.
- [x] Toàn bộ test suite pass 100%.
- [x] Sẵn sàng bàn giao cho người dùng.
