# SPEC-03: Thay Đổi Danh Mục Skin & Texture Mới (Duck & Phoenix Skins)

## 1. Objective
Nâng cấp và thay thế toàn bộ hệ thống texture/skin chim hiện tại trong Flappy Bird (Arcade 3.3.3) bằng bộ sprite pixel art mới từ thư mục `C:\Users\Admin\Desktop\ducks\trimmed`, ngoại trừ skin Angel Robin (`custom_robin`):

1. **Yellow Duck (`yellow`)**:
   - Texture: Sao chép từ `C:\Users\Admin\Desktop\ducks\trimmed\Yello.png` -> `assets/skins/yellow.png` (Kích thước gốc: $94 \times 56\text{ px}$, RGBA).
   - Phân loại: Mặc định (`unlock_type="default"`, `price=0`, `unlock_value=0`).
   - Tên hiển thị: `"Yellow Duck"`.
   - Mô tả: `"The friendly yellow duck."`.

2. **Lightning Blue (`electric`)**:
   - Texture: Sao chép từ `C:\Users\Admin\Desktop\ducks\trimmed\Electric Blue Pixel Bird Sprite.png` -> `assets/skins/electric.png` (Kích thước gốc: $47 \times 30\text{ px}$, RGBA).
   - Phân loại: Mua bằng coin trong Shop (`unlock_type="coin"`, `price=10`, `unlock_value=10`). Khi mua sẽ khấu trừ 10 coins trong ví.
   - Tên hiển thị: `"Lightning Blue"`.
   - Mô tả: `"Agile electric flyer (10 Coins)."`.

3. **Cybernetic (`cyber`)**:
   - Texture: Sao chép từ `C:\Users\Admin\Desktop\ducks\trimmed\Cybernetic Pixel Art Duck Sprite.png` -> `assets/skins/cyber.png` (Kích thước gốc: $44 \times 26\text{ px}$, RGBA).
   - Phân loại: Thành tựu điểm cao (`unlock_type="highscore"`, `price=0`, `unlock_value=25`). Tự động mở khi High Score $\ge 25$.
   - Tên hiển thị: `"Cybernetic"`.
   - Mô tả: `"Unlock at High Score >= 25."`.

4. **Royal Gold (`royal`)**:
   - Texture: Sao chép từ `C:\Users\Admin\Desktop\ducks\trimmed\Royal Golden Bird Pixel Sprite.png` -> `assets/skins/royal.png` (Kích thước gốc: $47 \times 32\text{ px}$, RGBA).
   - Phân loại: Thành tựu tích lũy (`unlock_type="total_coins"`, `price=0`, `unlock_value=100`). Tự động mở khi tổng xu nhặt được $\ge 100$.
   - Tên hiển thị: `"Royal Gold"`.
   - Mô tả: `"Unlock at Total Coins >= 100."`.

5. **Fiery Phoenix (`fiery`)**:
   - Texture: Sao chép từ `C:\Users\Admin\Desktop\ducks\trimmed\Fiery Pixel Phoenix Sprite.png` -> `assets/skins/fiery.png` (Kích thước gốc: $98 \times 65\text{ px}$, RGBA).
   - Phân loại: Thành tựu điểm cao (`unlock_type="highscore"`, `price=0`, `unlock_value=50`). Tự động mở khi High Score $\ge 50$.
   - Tên hiển thị: `"Fiery Phoenix"`.
   - Mô tả: `"Unlock at High Score >= 50."`.

6. **Angel Robin (`custom_robin`)** *(Bảo tồn)*:
   - Texture: Giữ nguyên `assets/skins/custom_robin.png` ($1023 \times 512\text{ px}$, RGBA).
   - Phân loại: Mặc định/Tùy chỉnh đặc biệt (`unlock_type="default"`, `price=0`, `unlock_value=0`).
   - Tên hiển thị: `"Angel Robin"`.
   - Mô tả: `"Angel Robin custom skin."`.

Thứ tự duyệt trong Shop:
`Yellow Duck` (1) $\to$ `Lightning Blue` (2) $\to$ `Cybernetic` (3) $\to$ `Royal Gold` (4) $\to$ `Fiery Phoenix` (5) $\to$ `Angel Robin` (6).

---

## 2. Tech Stack & Commands
- **Ngôn ngữ**: Python 3.14+
- **Game Engine**: Python Arcade 3.3.3
- **Thư viện xử lý ảnh**: Pillow
- **Testing**: Pytest 9.1.1

### Executable Commands:
```powershell
# Chạy game kiểm tra thực tế
python -m src.main

# Chạy toàn bộ test suite
python -m pytest

# Chạy riêng các bài test liên quan đến Skin và SaveData
python -m pytest tests/test_skin_manager.py tests/test_storage.py tests/test_crisp_rendering.py
```

---

## 3. Project Structure & File Changes

```text
e:\FlappyBird\
├── assets/
│   └── skins/
│       ├── yellow.png              # [MỚI] Sao chép từ Yello.png (94x56 RGBA)
│       ├── electric.png            # [MỚI] Sao chép từ Electric Blue... (47x30 RGBA)
│       ├── cyber.png               # [MỚI] Sao chép từ Cybernetic... (44x26 RGBA)
│       ├── royal.png               # [MỚI] Sao chép từ Royal Golden... (47x32 RGBA)
│       ├── fiery.png               # [MỚI] Sao chép từ Fiery Pixel... (98x65 RGBA)
│       ├── custom_robin.png        # [GIỮ NGUYÊN] Angel Robin
│       └── [classic, blue_bird, ...] # [LƯU TRỮ DỰ PHÒNG] Không xóa file cũ
├── src/
│   ├── models/
│   │   ├── skin.py                 # Cập nhật DEFAULT_SKINS sang 6 skin mới
│   │   └── save_data.py            # Cập nhật default="yellow", reset ID cũ, bảo lưu custom_robin
│   ├── services/
│   │   └── skin_manager.py         # Duy trì tương thích hoàn hảo logic mở khóa/mua
│   ├── views/
│   │   └── shop_view.py            # Cập nhật fallback texture về yellow.png
│   ├── main.py                     # Cập nhật fallback reload texture về yellow.png
└── tests/
    ├── test_skin_manager.py        # Cập nhật test theo các mốc 10 coin, HS 25, Total 100, HS 50
    ├── test_storage.py             # Cập nhật test migration/reset save data về yellow
    ├── test_crisp_rendering.py     # Cập nhật kích thước mong đợi của các skin mới
    └── test_duck_skins.py          # [MỚI] Kiểm tra chi tiết 6 skin mới, tỷ lệ auto-scale và hitbox
```

---

## 4. Code Style & Architecture Conventions

### Hitbox & Tự Động Co Giãn (Auto-Scaling):
- Trong `src/entities/bird.py`: Thực thể `Bird` tự động tính scale hiển thị:
  $$\text{scale} = \frac{\text{STANDARD\_HITBOX\_HEIGHT} (24.0\text{ px})}{\text{texture.height}}$$
- Đảm bảo chiều cao hiển thị trên màn hình luôn đồng nhất $24.0\text{ px}$ bất kể texture có kích thước $94 \times 56$ hay $98 \times 65$.
- Hitbox bất biến: Giữ nguyên hình chữ nhật $34 \times 24\text{ px}$ căn giữa theo tâm chim, không làm mất cân bằng gameplay.

### Save Data Reset & Sanitization:
```python
# Quy tắc chuẩn hóa save data khi đọc file save cũ (src/models/save_data.py):
# 1. Các skin hợp lệ hiện tại: {"yellow", "electric", "cyber", "royal", "fiery", "custom_robin"}
# 2. Bất kỳ skin cũ nào không nằm trong danh mục (classic, blue_bird, red_bird, cyber_bird, golden_bird)
#    sẽ bị xóa khỏi unlocked_skins.
# 3. Luôn bảo đảm "yellow" có mặt trong unlocked_skins.
# 4. Nếu "custom_robin" đã có trong unlocked_skins cũ, tiếp tục giữ nguyên.
# 5. Nếu equipped_skin là skin cũ không còn hợp lệ, fallback về "yellow".
```

---

## 5. Testing Strategy
- **Unit Test `test_skin_manager.py`**:
  - `yellow`: Luôn mở khóa mặc định (`is_unlocked = True`).
  - `electric`: Mua bằng 10 coin, trừ đúng 10 coin, không mua được nếu thiếu coin.
  - `cyber`: Tự động mở khi `high_score >= 25`.
  - `royal`: Tự động mở khi `total_coins_collected >= 100`.
  - `fiery`: Tự động mở khi `high_score >= 50`.
  - `custom_robin`: Mở khóa mặc định (`is_unlocked = True`).
- **Data Persistence Test `test_storage.py`**:
  - Đọc file save chứa dữ liệu cũ (`classic`, `blue_bird`) $\to$ Khởi tạo lại `unlocked_skins` sạch sẽ (`yellow` + `custom_robin` nếu có).
  - Lưu và nạp lại trạng thái mới nguyên vẹn.
- **Graphic Quality Test `test_crisp_rendering.py` & `test_duck_skins.py`**:
  - Xác nhận 5 file ảnh mới tồn tại, đúng định dạng `RGBA`.
  - Kích thước ảnh khớp tuyệt đối với file gốc từ desktop.
  - Kiểm tra `Bird` scale và hitbox $34 \times 24$ không bị lệch.

---

## 6. Boundaries

### Always Do:
- Bảo toàn tuyệt đối skin Angel Robin (`custom_robin.png`) và thông số của nó.
- Giữ nguyên các file texture cũ trong `assets/skins/` làm dự phòng (không xóa vật lý).
- Chạy toàn bộ test suite `python -m pytest` và đảm bảo 100% pass trước khi nghiệm thu.

### Ask First:
- Thay đổi bất kỳ thông số vật lý nào của chim hoặc cơ chế sinh chướng ngại vật/ống nước.
- Xóa tiến trình coin (`coins`, `total_coins_collected`) hoặc `high_score` của người chơi.

### Never Do:
- Không dùng code dở dang, code giả lập hoặc placeholder.
- Không để hitbox của chim thay đổi theo kích thước của texture mới.
- Không xóa nhầm file `custom_robin.png`.

---

## 7. Success Criteria
1. Tải và nạp thành công 5 sprite mới vào `assets/skins/`.
2. Màn hình Shop hiển thị chuẩn xác 6 skin với tên tiếng Anh, mô tả retro và trạng thái khóa/mở khóa.
3. Người chơi có thể trang bị và bay trong game bằng từng skin mới mà không gặp lỗi hiển thị hay va chạm lệch.
4. Mọi test suite hiện có và bài test mới đều pass 100%.

---

## 8. Open Questions & Assumptions
- **Assumptions confirmed with user**:
  - Skin ID chuẩn hóa: `yellow`, `electric`, `cyber`, `royal`, `fiery` + `custom_robin`.
  - Lưu trữ file texture: Tên chuẩn hóa theo ID (`yellow.png`, `electric.png`, ...), giữ file cũ làm backup.
  - Điều kiện mở khóa: Lightning Blue mua bằng 10 xu trong Shop (trừ ví xu), Royal Gold tự mở khi tích lũy 100 xu, Cybernetic mở khi High Score $\ge 25$, Fiery Phoenix mở khi High Score $\ge 50$.
  - Ngôn ngữ Shop: Phong cách tiếng Anh retro chuẩn arcade đồng bộ với giao diện hiện tại.
  - Thứ tự hiển thị: Yellow Duck $\to$ Lightning Blue $\to$ Cybernetic $\to$ Royal Gold $\to$ Fiery Phoenix $\to$ Angel Robin.
  - SaveData: Reset danh sách skin về mặc định (`yellow`), giữ lại `custom_robin` nếu đã có.
- Không còn câu hỏi mở nào chưa được giải quyết.
