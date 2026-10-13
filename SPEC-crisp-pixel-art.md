# SPEC-02: Đồ Họa Pixel Art Sắc Nét & Tích Hợp Assets Gốc (Crisp Pixel Art & Authentic Assets)

## 1. Objective
Hiện đại hóa hệ thống hiển thị và chất lượng mỹ thuật của trò chơi Flappy Bird (Arcade 3.3.3) trên branch `feat/crisp-pixel-art`:
- Loại bỏ hoàn toàn hiện tượng mờ nhòe (blurry/bilinear artifacts) khi phóng to cửa sổ hoặc chuyển Fullscreen bằng cách kích hoạt cơ chế lọc texture **Nearest-Neighbor (`GL_NEAREST`)** trong Arcade Engine.
- Tích hợp bộ assets sprite pixel art gốc từ thư mục tham khảo `E:\stolen\FlapPyBird\assets\sprites` (nền ngày/đêm, ống xanh/đỏ, mặt đất, giao diện gameover/message và bộ font số retro 0-9).
- Chuẩn hóa các skin chim tĩnh (`classic`, `blue_bird`, `red_bird`) từ các sprite gốc (`midflap`) với kích thước chuẩn $34 \times 24\text{ px}$, không thêm animation vỗ cánh theo yêu cầu người dùng.
- Bảo toàn tuyệt đối hệ trục tọa độ thế giới ảo $288 \times 512$, hệ số động học vật lý, hitbox cố định $34 \times 24$, hệ thống kinh tế/save data, và giữ vững 100% test suite đang có (40 tests).

---

## 2. Tech Stack & Dependencies
- **Ngôn ngữ**: Python 3.14+
- **Game Engine**: `arcade == 3.3.3` (Sử dụng `arcade.Window`, `arcade.camera.Camera2D`, `arcade.SpriteList`, `TextureAtlas`, `pyglet.gl`)
- **Đồ họa**: `pillow` (đọc, chuẩn hóa định dạng Palette `P` sang `RGBA`, lưu sprite PNG)
- **Hệ thống kiểm thử**: `pytest == 9.1.1`

---

## 3. Commands
- **Chạy game**: `python -m src.main`
- **Chạy toàn bộ test suite**: `python -m pytest`
- **Chạy test đồ họa & texture filter**: `python -m pytest tests/test_crisp_rendering.py`
- **Công cụ đồng bộ asset**: `python -m src.tools.import_authentic_assets`

---

## 4. Project Structure Changes
```text
e:\FlappyBird\
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
│       ├── cyber_bird.png          # [Giữ nguyên] 48x32 RGBA skin đặc biệt
│       └── golden_bird.png         # [Giữ nguyên] 64x64 RGBA skin vương miện
├── src/
│   ├── main.py                     # Cấu hình GL_NEAREST cho default_atlas & window texture filter
│   ├── views/
│   │   ├── base_view.py            # Đảm bảo Camera2D duy trì Nearest-Neighbor filtering
│   │   ├── game_view.py            # Hiển thị điểm số bằng sprite số retro 0-9 thay cho text mờ
│   │   ├── start_view.py           # Dùng message.png chuẩn Flappy Bird
│   │   └── game_over_view.py       # Dùng gameover.png chuẩn Flappy Bird
│   └── tools/
│       ├── generate_placeholders.py# Sửa ensure_assets_exist: Không ghi đè asset thật nếu đã có
│       └── import_authentic_assets.py # Tool copy và convert P -> RGBA từ E:\stolen\FlapPyBird
└── tests/
    └── test_crisp_rendering.py     # Kiểm thử tự động texture filter GL_NEAREST & định dạng asset
```

---

## 5. Code Style & Technical Details

### 5.1. Cấu hình Nearest-Neighbor Texture Filtering (Chống Mờ Nhòe)
Arcade 3.x sử dụng `TextureAtlas` làm bộ đệm gom texture. Mặc định bộ lọc là `GL_LINEAR` khiến sprite phóng to bị nhòe.
Để pixel art sắc nét 100%:
```python
import pyglet.gl as gl
import arcade

# 1. Gán filter mặc định cho các SpriteList khởi tạo sau này
arcade.SpriteList.DEFAULT_TEXTURE_FILTER = (gl.GL_NEAREST, gl.GL_NEAREST)

# 2. Cấu hình Atlas mặc định của context cửa sổ
class FlappyWindow(arcade.Window):
    def __init__(self, ...) -> None:
        super().__init__(..., antialiasing=False)
        # Ép texture atlas chính dùng Nearest-Neighbor
        self.ctx.default_atlas.texture.filter = (gl.GL_NEAREST, gl.GL_NEAREST)
```

### 5.2. Chuẩn hóa định dạng Assets khi Import
Repo tham khảo lưu PNG ở bảng màu indexed 8-bit (`mode='P'`). Khi nạp vào Arcade có thể gây mất kênh trong suốt (transparency/alpha).
Hàm import bắt buộc chuyển đổi sang `RGBA`:
```python
from PIL import Image

def convert_and_save(src_path: Path, dst_path: Path) -> None:
    with Image.open(src_path) as img:
        rgba_img = img.convert("RGBA")
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        rgba_img.save(dst_path, "PNG")
```

### 5.3. Render Điểm Số Bằng Sprite Số Retro (`0.png` - `9.png`)
Thay vì dùng `arcade.Text` phụ thuộc vào rasterize font chữ vector của OS:
- Tạo một helper `ScoreSpriteGroup` quản lý danh sách sprite số $24 \times 36\text{ px}$.
- Khi điểm số thay đổi (ví dụ `score = 15`), chuyển thành chuỗi `"15"`, căn giữa màn hình tại $Y = \text{SCREEN\_HEIGHT} - 60$, đặt các sprite số `1.png` và `5.png` liền kề nhau.
- Điểm số hiển thị retro pixel-perfect như bản gốc Flappy Bird.

---

## 6. Testing Strategy
1. **Test Texture Filter (`test_crisp_rendering.py`)**:
   - Khởi tạo `FlappyWindow(visible=False)`.
   - Xác minh `window.ctx.default_atlas.texture.filter == (gl.GL_NEAREST, gl.GL_NEAREST)`.
   - Xác minh các `SpriteList` trong `GameView` (bg_list, pipe_list, bird_list, floor_list) đều sử dụng bộ lọc `GL_NEAREST`.
2. **Test Tính Toàn Vẹn Của Assets**:
   - Kiểm tra các file sprite chính (`background-day.png`, `base.png`, `pipe-green.png`, `classic.png`, các số `0.png`-`9.png`) tồn tại.
   - Kiểm tra kích thước chính xác:
     + Background: $(288, 512)$
     + Base: $(336, 112)$
     + Pipe: $(52, 320)$
     + Chim classic: $(34, 24)$
     + Các số: Chiều cao $36\text{ px}$
   - Kiểm tra chế độ màu (image mode) là `RGBA`.
3. **Regression Tests**:
   - Toàn bộ 40 unit test hiện có trong thư mục `tests/` phải tiếp tục pass 100%.

---

## 7. Boundaries
- **Always**:
  - Giữ nguyên chim ở dạng tĩnh 1 frame (`midflap`), không thêm animation vỗ cánh chu kỳ theo đúng yêu cầu người dùng.
  - Chuyển đổi mọi file PNG nhập từ repo tham khảo sang chuẩn `RGBA` trước khi nạp vào engine.
  - Giữ nguyên hằng số kích thước ảo $288 \times 512$, hitbox $34 \times 24$ và toàn bộ tham số vật lý.
  - Chạy `python -m pytest` kiểm tra 100% test pass trước khi hoàn tất.
- **Ask First**:
  - Thay đổi vị trí hoặc kích thước các nút bấm trong `ShopView` hay `GameOverView`.
- **Never**:
  - Không sửa đổi hay làm lệch các hằng số vật lý (`GRAVITY`, `FLAP_VELOCITY`, `PIPE_SPEED`).
  - Không để code `generate_placeholders.py` tự ý ghi đè làm mất asset gốc.

---

## 8. Success Criteria
- [ ] Khởi chạy game `python -m src.main`, hình ảnh hiển thị sắc nét, pixel art vuông vắn rõ ràng, không còn mờ nhòe ở cả cửa sổ thường lẫn Fullscreen (`F11`).
- [ ] Nền trời, ống nước, mặt đất và chim mang đúng phong cách đồ họa của Flappy Bird gốc.
- [ ] Chim có texture tĩnh sắc nét (classic = vàng, blue_bird = xanh, red_bird = đỏ), không có animation đập cánh phức tạp.
- [ ] Điểm số trong màn chơi hiển thị bằng bộ số pixel retro `0.png` - `9.png`.
- [ ] Màn hình Start và Game Over tích hợp sprite gốc `message.png` và `gameover.png`.
- [ ] Toàn bộ 40 test cũ + test crisp rendering mới vượt qua (100% Passed).

---

## 9. Assumptions & Open Questions

### Assumptions
1. Nguồn sprite tham khảo tại `E:\stolen\FlapPyBird\assets\sprites` đã đầy đủ và có sẵn trên máy cục bộ.
2. Skin chim tĩnh sẽ sử dụng frame `midflap` (tư thế vỗ cánh ngang cân bằng, đặc trưng nhất của Flappy Bird).
3. Hai skin đặc biệt mở khóa sau này (`cyber_bird` và `golden_bird`) sẽ giữ nguyên thiết kế hiện tại hoặc đồng bộ palette pixel để không mất tính năng của hệ thống Shop.

### Open Questions
1. **Hiển thị điểm số:** Bạn có muốn dùng bộ số sprite retro (`0.png` - `9.png`) thay thế hoàn toàn cho text điểm số hiện tại, hay muốn giữ lại `arcade.Text` với font retro? *(Khuyến nghị: Dùng bộ số sprite `0-9.png` gốc để đồ họa đồng bộ 100% retro)*.
2. **Skin Shop:** Hai skin mở khóa nâng cao (`cyber_bird` và `golden_bird`) hiện đang vẽ bằng code procedural. Bạn muốn giữ nguyên chúng hay điều chỉnh lại cho cùng phong cách pixel art của chim vàng/xanh/đỏ?
