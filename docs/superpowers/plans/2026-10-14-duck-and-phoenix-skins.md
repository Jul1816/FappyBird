# Duck & Phoenix Skins Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Thay thế toàn bộ hệ thống skins và texture chim cũ (trừ Angel Robin `custom_robin`) bằng 5 texture mới từ `C:\Users\Admin\Desktop\ducks\trimmed`, cập nhật cơ chế mở khóa và reset SaveData an toàn.

**Architecture:** Chuẩn hóa 5 texture mới sang RGBA tại `assets/skins/` (`yellow.png`, `electric.png`, `cyber.png`, `royal.png`, `fiery.png`). Cập nhật danh mục `DEFAULT_SKINS` trong `src/models/skin.py` với các mốc unlock tương ứng (default, coin 10, highscore 25, total_coins 100, highscore 50, Angel Robin). Cập nhật `src/models/save_data.py` để tự động lọc bỏ các ID cũ, reset về `yellow`, bảo lưu `custom_robin`, và cập nhật toàn bộ test suite.

**Tech Stack:** Python 3.14+, Python Arcade 3.3.3, Pillow (PIL), Pytest 9.1.1.

**Spec:** [SPEC-duck-skins.md](file:///e:/FlappyBird/SPEC-duck-skins.md)

---

## Global Constraints
- Skin IDs chuẩn: `yellow`, `electric`, `cyber`, `royal`, `fiery`, `custom_robin`.
- Texture format: Tất cả texture phải là RGBA và nằm trong thư mục `assets/skins/`.
- Hitbox bất biến: Thực thể `Bird` luôn có kích thước hiển thị cao $24.0\text{ px}$ và hitbox cố định $34 \times 24\text{ px}$.
- SaveData an toàn: Mặc định `equipped_skin="yellow"`, `unlocked_skins=["yellow"]`; loại bỏ các ID cũ khỏi save file nhưng giữ lại `custom_robin` nếu người chơi đã sở hữu.
- Test coverage: 100% pass với lệnh `python -m pytest`, không có test nào bị skip hoặc fail.

---

## Review Focus
1. **SaveData migration với save file cũ**: File save có `equipped_skin="classic"` hoặc `"blue_bird"` phải tự động fallback về `"yellow"` mà không gây crash.
2. **Bảo tồn Angel Robin**: File save có `"custom_robin"` phải giữ nguyên quyền sở hữu và trang bị được bình thường.
3. **Mua Lightning Blue bằng coin**: Khi mua `electric` (10 coins), số coin trong ví bị trừ 10; không được mua nếu số coin < 10.
4. **Tự động mở khóa thành tựu**: `cyber` tự mở khi High Score $\ge 25$; `royal` tự mở khi Total Coins $\ge 100$; `fiery` tự mở khi High Score $\ge 50$.
5. **Hitbox & Auto-scale**: Texture kích thước lớn (như $98 \times 65$ của `fiery` hay $94 \times 56$ của `yellow`) không được làm phình to hitbox hay va chạm sai lệch trong game.

---

## Task List

### Task 1: Asset Pipeline & Sprite Migration
**Files:**
- Create: `src/tools/import_duck_assets.py`
- Target Assets:
  - `assets/skins/yellow.png` (từ `Yello.png`)
  - `assets/skins/electric.png` (từ `Electric Blue Pixel Bird Sprite.png`)
  - `assets/skins/cyber.png` (từ `Cybernetic Pixel Art Duck Sprite.png`)
  - `assets/skins/royal.png` (từ `Royal Golden Bird Pixel Sprite.png`)
  - `assets/skins/fiery.png` (từ `Fiery Pixel Phoenix Sprite.png`)
- Test: `tests/test_duck_assets.py`

**Interfaces:**
- Consumes: Files trong `C:\Users\Admin\Desktop\ducks\trimmed`
- Produces: 5 file PNG chuẩn RGBA tại `assets/skins/`

- [ ] **Step 1: Write the failing test**
  Tạo `tests/test_duck_assets.py` kiểm tra sự tồn tại và định dạng RGBA của 5 file texture mới.
- [ ] **Step 2: Run test to verify it fails**
  Chạy `python -m pytest tests/test_duck_assets.py` và xác nhận FAIL vì file chưa được copy.
- [ ] **Step 3: Implement `import_duck_assets.py`**
  Viết script đọc từ `C:\Users\Admin\Desktop\ducks\trimmed`, chuyển sang RGBA nếu cần, lưu vào `assets/skins/` với tên chuẩn (`yellow.png`, `electric.png`, `cyber.png`, `royal.png`, `fiery.png`), không đụng vào `custom_robin.png` và các file cũ. Chạy script để tạo asset.
- [ ] **Step 4: Run test to verify it passes**
  Chạy `python -m pytest tests/test_duck_assets.py` và xác nhận PASS.
- [ ] **Step 5: Commit**
  `git add assets/skins/ tests/test_duck_assets.py src/tools/import_duck_assets.py && git commit -m "feat(assets): import new duck and phoenix skin textures"`

---

### Task 2: Skin Catalog & Model Configuration
**Files:**
- Modify: `src/models/skin.py`
- Test: `tests/test_skin_manager.py`

**Interfaces:**
- Consumes: Các file sprite trong `assets/skins/`
- Produces: `DEFAULT_SKINS: list[Skin]` gồm 6 skin (`yellow`, `electric`, `cyber`, `royal`, `fiery`, `custom_robin`) với giá, điều kiện mở khóa và mô tả chuẩn retro.

- [ ] **Step 1: Write the failing test**
  Cập nhật `tests/test_skin_manager.py` kiểm tra danh mục 6 skin mới, điều kiện mở khóa của `electric` (10 coins), `cyber` (HS 25), `royal` (Total 100), `fiery` (HS 50).
- [ ] **Step 2: Run test to verify it fails**
  Chạy `python -m pytest tests/test_skin_manager.py` và xác nhận FAIL do danh mục hiện tại vẫn là `classic`, `blue_bird`, v.v.
- [ ] **Step 3: Update `src/models/skin.py`**
  Cập nhật `DEFAULT_SKINS` đúng thứ tự:
  1. `yellow`: Yellow Duck, default, price 0
  2. `electric`: Lightning Blue, coin, price 10
  3. `cyber`: Cybernetic, highscore, req 25
  4. `royal`: Royal Gold, total_coins, req 100
  5. `fiery`: Fiery Phoenix, highscore, req 50
  6. `custom_robin`: Angel Robin, default, price 0
- [ ] **Step 4: Run test to verify it passes**
  Chạy `python -m pytest tests/test_skin_manager.py` và xác nhận PASS.
- [ ] **Step 5: Commit**
  `git add src/models/skin.py tests/test_skin_manager.py && git commit -m "feat(models): update DEFAULT_SKINS to new duck and phoenix catalog"`

---

### Task 3: SaveData Backward Compatibility & Reset Logic
**Files:**
- Modify: `src/models/save_data.py`
- Test: `tests/test_storage.py`

**Interfaces:**
- Consumes: JSON từ `data/save_data.json`
- Produces: `SaveData` đã được khử khuẩn (sanitized), loại bỏ skin cũ, fallback `equipped_skin` về `"yellow"` nếu là skin cũ, bảo lưu `"custom_robin"` nếu có.

- [ ] **Step 1: Write the failing test**
  Cập nhật `tests/test_storage.py` bổ sung test case nạp save data cũ (chứa `classic`, `blue_bird`, `red_bird`) $\to$ kỳ vọng `unlocked_skins` chỉ chứa `yellow`, và test case có `custom_robin` $\to$ kỳ vọng giữ lại `custom_robin`.
- [ ] **Step 2: Run test to verify it fails**
  Chạy `python -m pytest tests/test_storage.py` và xác nhận FAIL.
- [ ] **Step 3: Update `src/models/save_data.py`**
  Cập nhật `SaveData`:
  - `equipped_skin: str = "yellow"`
  - `unlocked_skins: list[str] = field(default_factory=lambda: ["yellow"])`
  - Trong `from_dict`: Lọc bỏ danh sách ID cũ `{"classic", "blue_bird", "red_bird", "cyber_bird", "golden_bird"}`. Luôn bảo đảm `"yellow"` có trong `unlocked_skins`. Giữ lại `"custom_robin"` nếu có. Nếu `equipped_skin` không nằm trong danh mục mới hợp lệ, gán về `"yellow"`.
- [ ] **Step 4: Run test to verify it passes**
  Chạy `python -m pytest tests/test_storage.py` và xác nhận PASS.
- [ ] **Step 5: Commit**
  `git add src/models/save_data.py tests/test_storage.py && git commit -m "feat(storage): implement legacy skin reset and yellow default fallback in SaveData"`

---

### Task 4: View Integration & Fallback Updates
**Files:**
- Modify: `src/views/shop_view.py`
- Modify: `src/main.py`
- Test: `tests/test_e2e_views.py`

**Interfaces:**
- Consumes: `SkinManager`, `DEFAULT_SKINS`
- Produces: Màn hình Shop và Game hiển thị đúng 6 skin mới, fallback texture là `yellow.png`.

- [ ] **Step 1: Write the failing test**
  Cập nhật `tests/test_e2e_views.py` để kiểm tra Shop hiển thị `yellow` làm skin mặc định, test mua `electric` với 10 xu, kiểm tra auto-unlock `cyber` khi High Score $\ge 25$.
- [ ] **Step 2: Run test to verify it fails**
  Chạy `python -m pytest tests/test_e2e_views.py` và xác nhận FAIL.
- [ ] **Step 3: Update `src/views/shop_view.py` & `src/main.py`**
  - Trong `src/views/shop_view.py`: Thay đổi fallback `load_texture` từ `classic.png` sang `yellow.png`.
  - Trong `src/main.py`: Thay đổi fallback `reload_skin_texture` sang `yellow.png`.
- [ ] **Step 4: Run test to verify it passes**
  Chạy `python -m pytest tests/test_e2e_views.py` và xác nhận PASS.
- [ ] **Step 5: Commit**
  `git add src/views/shop_view.py src/main.py tests/test_e2e_views.py && git commit -m "feat(views): update shop and main view fallback texture to yellow.png"`

---

### Task 5: Hitbox Integrity, Crisp Rendering & Full Regression
**Files:**
- Modify: `tests/test_crisp_rendering.py`
- Create: `tests/test_duck_skins.py` (thay thế chức năng của `test_golden_crown.py`)
- Remove / Refactor: `tests/test_golden_crown.py`

**Interfaces:**
- Consumes: Tất cả 6 skins mới
- Produces: 100% test suite pass

- [ ] **Step 1: Write the failing test**
  Cập nhật `tests/test_crisp_rendering.py` kiểm tra đúng 5 file skin mới cùng kích thước thực tế của chúng ($94 \times 56$, $47 \times 30$, $44 \times 26$, $47 \times 32$, $98 \times 65$) và `custom_robin.png` ($1023 \times 512$).
  Tạo `tests/test_duck_skins.py` kiểm tra việc nạp từng skin vào `Bird`, xác nhận `bird.height == 24.0 px` và hitbox chuẩn $34 \times 24\text{ px}$.
- [ ] **Step 2: Run test to verify it fails**
  Chạy `python -m pytest tests/test_crisp_rendering.py` và xác nhận FAIL do danh sách kích thước cũ.
- [ ] **Step 3: Update tests & remove obsolete tests**
  Cập nhật `tests/test_crisp_rendering.py` và refactor `tests/test_golden_crown.py` sang `tests/test_duck_skins.py`. Cập nhật `data/save_data.json` mẫu nếu cần.
- [ ] **Step 4: Run full test suite to verify all pass**
  Chạy `python -m pytest -v` đảm bảo toàn bộ các bài test đều PASS 100%.
- [ ] **Step 5: Commit**
  `git add tests/ && git commit -m "test: update regression and crisp rendering tests for new duck skin catalog"`

---

## Checkpoint: Final Verification
- [ ] Toàn bộ 5 texture mới đã được copy và hoạt động ổn định.
- [ ] Cả 6 skin hiển thị mượt mà trong Shop theo đúng thứ tự.
- [ ] Logic mua và mở khóa tự động hoạt động chính xác theo spec.
- [ ] Hitbox và scale chim bất biến $34 \times 24$ px.
- [ ] Toàn bộ test suite `python -m pytest` đạt 100% PASS.
