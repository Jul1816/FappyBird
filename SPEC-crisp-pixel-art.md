# SPEC-02: Đồ Họa Pixel Art Sắc Nét, Tích Hợp Assets Gốc & Skin Tùy Chỉnh (Crisp Pixel Art & Custom Skin)

## 1. Objective
Hiện đại hóa toàn diện hệ thống hiển thị và chất lượng mỹ thuật của trò chơi Flappy Bird (Arcade 3.3.3) trên branch `feat/crisp-pixel-art`:
- Loại bỏ triệt để hiện tượng mờ nhòe (bilinear blur) khi hiển thị cửa sổ và Fullscreen bằng cơ chế lọc texture **Nearest-Neighbor (`GL_NEAREST`)** trong Arcade Engine.
- Tích hợp bộ assets sprite pixel art gốc từ thư mục tham khảo `E:\stolen\FlapPyBird\assets\sprites` (nền ngày/đêm, ống xanh/đỏ, mặt đất, giao diện gameover/message).
- Hiển thị điểm số bằng bộ số pixel retro `0.png` - `9.png` thay thế cho text vector OS.
- Chuẩn hóa các skin chim tĩnh (`classic`, `blue_bird`, `red_bird`) dạng 1 frame tĩnh (`midflap`, $34 \times 24\text{ px}$) không animation vỗ cánh theo yêu cầu.
- Tinh chỉnh lại hai skin đặc biệt `cyber_bird` (chim cơ khí kính visor neon) và `golden_bird` (chim hoàng kim vương miện) trên nền pixel art chuẩn sắc nét.
- **Thử nghiệm tính năng Custom Skin**: Tích hợp texture người dùng tải lên (Robin Thiên Thần chibi pixel art) thành skin chính thức `angel_robin`, hỗ trợ cơ chế tự động cân đối kích thước hiển thị (auto-scaling) và duy trì Hitbox bất biến $34 \times 24\text{ px}$.
- Bảo toàn tuyệt đối hệ trục tọa độ thế giới ảo $288 \times 512$, hệ số động học vật lý và đảm bảo 100% test suite tiếp tục pass.

---

## 2. Tech Stack & Dependencies
- **Ngôn ngữ**: Python 3.14+
- **Game Engine**: `arcade == 3.3.3` (`arcade.Window`, `arcade.camera.Camera2D`, `arcade.SpriteList`, `TextureAtlas`, `pyglet.gl`)
- **Đồ họa**: `pillow` (xử lý chuyển đổi màu Palette `P` -> `RGBA`, rescale sprite pixel art)
- **Hệ thống kiểm thử**: `pytest == 9.1.1`

---

## 3. Commands
- **Chạy game**: `python -m src.main`
- **Chạy toàn bộ test suite**: `python -m pytest`
- **Chạy test đồ họa & custom skin**: `python -m pytest tests/test_crisp_rendering.py`
- **Công cụ đồng bộ asset**: `python -m src.tools.import_authentic_assets`

---

## 4. Project Structure Changes
```text
e:\FlappyBird/
├── assets/
│   ├── sprites/
│   │   ├── background-day.png      # [Đổi mới] 288x512 RGBA pixel art gốc
│   │   ├── background-night.png    # [Đổi mới] 288x512 RGBA pixel art gốc
│   │   ├── base.png                # [Đổi mới] 336x112 RGBA pixel art gốc
│   │   ├── pipe-green.png          # [Đổi mới] 52x320 RGBA pixel art gốc
│   │   ├── pipe-red.png            # [Đổi mới] 52x320 RGBA pixel art gốc
│   │   ├── message.png             # [Thêm mới] 184x267 RGBA (Màn hình Get Ready)
│   │   ├── gameover.png            # [Thêm mới] 192x42 RGBA (Banner Game Over)
│   │   └── digits/                 # [Thêm mới] 0.png đến 9.png (Font số retro 24x36)
│   └── skins/
│       ├── classic.png             # [Đổi mới] 34x24 RGBA từ yellowbird-midflap
│       ├── blue_bird.png           # [Đổi mới] 34x24 RGBA từ bluebird-midflap
│       ├── red_bird.png            # [Đổi mới] 34x24 RGBA từ redbird-midflap
│       ├── cyber_bird.png          # [Tinh chỉnh] 34x24 RGBA pixel art chim cơ khí kính visor
│       ├── golden_bird.png         # [Tinh chỉnh] 34x24 RGBA pixel art chim hoàng kim vương miện
│       └── angel_robin.png         # [Thêm mới] 64x32 RGBA skin tùy chỉnh (Robin Thiên Thần)
├── src/
│   ├── entities/
│   │   ├── bird.py                 # Hỗ trợ tự động scale hiển thị theo kích thước texture nếu > 36px
│   │   └── score_display.py        # [Thêm mới] Quản lý sprite chuỗi số retro 0-9
│   ├── models/
│   │   └── skin.py                 # Thêm skin angel_robin vào DEFAULT_SKINS
│   ├── views/
│   │   ├── base_view.py            # Đảm bảo Camera2D duy trì Nearest-Neighbor filtering
│   │   ├── game_view.py            # Tích hợp ScoreDisplay (sprite số 0-9)
│   │   ├── start_view.py           # Dùng message.png chuẩn Flappy Bird
│   │   ├── game_over_view.py       # Dùng gameover.png chuẩn Flappy Bird
│   │   └── shop_view.py            # Xem trước và trang bị được cả skin tùy chỉnh kích thước lớn
│   └── tools/
│       ├── generate_placeholders.py# Sửa ensure_assets_exist: Không ghi đè asset thật nếu đã có
│       └── import_authentic_assets.py # Copy, convert RGBA và tối ưu skin Robin từ ảnh upload
└── tests/
    └── test_crisp_rendering.py     # Test texture filter GL_NEAREST, format RGBA, và custom skin
```

---

## 5. Architectural & Implementation Details

### 5.1. Cấu hình Nearest-Neighbor Texture Filtering (GL_NEAREST)
```python
import pyglet.gl as gl
import arcade

# Áp dụng cho mọi SpriteList tạo mới
arcade.SpriteList.DEFAULT_TEXTURE_FILTER = (gl.GL_NEAREST, gl.GL_NEAREST)

class FlappyWindow(arcade.Window):
    def __init__(self, ...) -> None:
        super().__init__(..., antialiasing=False)
        # Ép texture atlas chính dùng Nearest-Neighbor
        self.ctx.default_atlas.texture.filter = (gl.GL_NEAREST, gl.GL_NEAREST)
```

### 5.2. Hiển thị Điểm Số Bằng Sprite Số Retro Đa Chữ Số (`ScoreDisplay`)
- Quản lý `arcade.SpriteList` chứa các chữ số tạo từ `assets/sprites/digits/{digit}.png` (chiều cao $36\text{ px}$, số `1` rộng $16\text{ px}$, các số khác rộng $24\text{ px}$).
- **Thuật toán căn giữa tự động cho điểm số 1, 2, 3... chữ số**:
  1. Khi `score` thay đổi (ví dụ: `0`, `14`, `108`), chuyển thành chuỗi các ký tự số.
  2. Tính tổng chiều rộng của toàn bộ chuỗi số:
     $$\text{total\_width} = \sum_{i=1}^{k} \text{width}(\text{digit}_i)$$
  3. Xác định tọa độ $X$ bắt đầu bên trái:
     $$X_{\text{start}} = \frac{\text{SCREEN\_WIDTH} - \text{total\_width}}{2.0}$$
  4. Lần lượt định vị tâm của từng sprite số từ trái qua phải:
     $$X_{\text{digit}} = X_{\text{current}} + \frac{\text{width}(\text{digit})}{2.0}, \quad Y_{\text{digit}} = \text{SCREEN\_HEIGHT} - 60.0$$
     $$X_{\text{current}} = X_{\text{current}} + \text{width}(\text{digit})$$
  5. Kết quả: Điểm số luôn luôn nằm chính giữa màn hình thế giới ảo theo trục dọc ($X = 144.0$) một cách hoàn hảo, bất kể số lượng chữ số tăng lên bao nhiêu.

### 5.3. Cơ Chế Custom Skin Chuẩn Hóa Theo Chiều Cao Hitbox
- **Nguyên tắc bảo toàn độ phân giải file**:
  - File texture trên đĩa (kể cả file ngoài người dùng thêm vào như `custom_robin.png` kích thước $1023 \times 512\text{ px}$) được giữ nguyên vẹn 100% độ phân giải gốc, **không qua resize hay nén ảnh bằng Pillow**.
- **Công thức Auto-Fit chiều cao hiển thị bằng đúng chiều cao Hitbox thực tế**:
  - Trong `Bird` entity, khi nhận bất kỳ texture nào có kích thước bất kỳ ($32\times32$, $64\times64$, $48\times32$, $1:1$, $2:1$, $1023\times512$), hệ thống tự động tính tỷ lệ hiển thị `scale`:
    $$\text{scale} = \frac{\text{STANDARD\_HITBOX\_HEIGHT}}{\text{texture.height}} = \frac{24.0}{\text{texture.height}}$$
  - **Kích thước hiển thị trên màn hình**:
    + Chiều cao hiển thị: $\text{rendered\_height} = \text{texture.height} \times \text{scale} = 24.0\text{ px}$ (bằng khít chiều cao hitbox thực tế).
    + Chiều rộng hiển thị: $\text{rendered\_width} = \text{texture.width} \times \text{scale} = \text{texture.width} \times \frac{24.0}{\text{texture.height}}$ (bảo toàn tỷ lệ khung hình gốc).
    + Ví dụ với ảnh Robin $1023 \times 512$: $\text{scale} = \frac{24.0}{512} \approx 0.046875 \implies \text{rendered\_height} = 24.0\text{ px}, \text{rendered\_width} \approx 48.0\text{ px}$.
- **Căn giữa Hitbox hoàn hảo trong Skin**:
  - Hitbox chuẩn cố định $34 \times 24\text{ px}$ được đặt chính giữa tâm của texture (`center_x, center_y`):
    $$\text{Hitbox} = [(-17.0, -12.0), (17.0, -12.0), (17.0, 12.0), (-17.0, 12.0)]$$
  - Viền trên và viền dưới của hitbox khớp khít với đỉnh và đáy của skin ($Y \in [-12, +12]$).
  - Trọng tâm và khuôn mặt nhân vật nằm trọn vẹn trong vùng hitbox va chạm.
- **Áp dụng đồng bộ cho `ShopView`**:
  - Trong màn hình xem trước Shop, sprite preview tự động tính theo tỷ lệ chuẩn `base_scale = 24.0 / texture.height` nhân với hệ số phóng đại preview ($1.5 \times$), giúp mọi skin từ $32\times32$ đến $1023\times512$ đều hiển thị vừa vặn, đẹp mắt trong khung giao diện.
- **Cấu hình trong `DEFAULT_SKINS`**:
  ```python
  Skin(
      id="custom_robin",
      name="Robin Thiên Thần (Custom)",
      price=0,
      unlock_type="default",
      unlock_value=0,
      sprite_path=str(ASSETS_DIR / "skins" / "custom_robin.png"),
      description="Skin tùy chỉnh thử nghiệm: Robin Thiên Thần thu nhỏ khớp chuẩn chiều cao hitbox 24px.",
  )
  ```

### 5.4. Tinh chỉnh `cyber_bird` và `golden_bird`
- Lấy nền tảng sprite pixel art gốc từ Flappy Bird ($34 \times 24\text{ px}$).
- Tinh chỉnh pixel art:
  - `cyber_bird`: Kính visor công nghệ xanh ngọc (`#00FFC8`) và viền giáp kim loại.
  - `golden_bird`: Vương miện vàng ngọc đỏ trên đầu và thân chim phủ sắc kim rực rỡ.

---

## 6. Testing Strategy
1. **Test Texture Filter (`test_crisp_rendering.py`)**:
   - Kiểm tra `window.ctx.default_atlas.texture.filter == (gl.GL_NEAREST, gl.GL_NEAREST)`.
   - Kiểm tra các `SpriteList` trong game duy trì bộ lọc Nearest-Neighbor.
2. **Test Assets & Custom Skin**:
   - Kiểm tra các assets gốc và skin `angel_robin.png` tồn tại, định dạng `RGBA`.
   - Kiểm tra kích thước chính xác ($64 \times 32$ cho Robin, $34 \times 24$ cho chim gốc, $24 \times 36$ cho digits).
   - Kiểm tra hitbox của chim khi mang skin `angel_robin` vẫn là $34 \times 24$.
3. **Regression Tests**:
   - Đảm bảo toàn bộ 40 tests hiện tại tiếp tục pass 100%.

---

## 7. Boundaries
- **Always**:
  - Giữ chim ở dạng 1 frame tĩnh (`midflap`), không thêm animation vỗ cánh.
  - Chuyển đổi mọi file PNG sang `RGBA`.
  - Giữ nguyên hằng số kích thước ảo $288 \times 512$, hitbox $34 \times 24$ và toàn bộ tham số vật lý.
  - Chạy `python -m pytest` kiểm tra 100% test pass.
- **Ask First**:
  - Thay đổi thông số giá coin mở khóa của các skin có sẵn.
- **Never**:
  - Không thay đổi các hằng số vật lý (`GRAVITY`, `FLAP_VELOCITY`).
  - Không để code `generate_placeholders.py` ghi đè làm mất asset thật.

---

## 8. Success Criteria
- [ ] Khởi chạy game `python -m src.main`, hình ảnh sắc nét tuyệt đối, không còn mờ nhòe ở cả cửa sổ thường và Fullscreen (`F11`).
- [ ] Điểm số hiển thị bằng bộ số pixel retro `0.png` - `9.png` căn giữa đẹp mắt.
- [ ] Màn hình Start và Game Over tích hợp sprite gốc `message.png` và `gameover.png`.
- [ ] Hai skin `cyber_bird` và `golden_bird` mang phong cách pixel art sắc nét đồng bộ.
- [ ] Skin `angel_robin` xuất hiện trong Shop, người chơi có thể trang bị và bay thử mượt mà qua các cột ống với hitbox chuẩn xác $34 \times 24$.
- [ ] Toàn bộ 40 test cũ + test crisp rendering mới vượt qua (100% Passed).

---

## 9. Open Questions & Assumptions
- Mọi câu hỏi thiết kế đã được giải quyết và thống nhất qua phản hồi của bạn.
- Không còn câu hỏi mở nào tồn tại.
