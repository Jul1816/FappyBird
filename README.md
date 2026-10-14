# Flappy Bird Pixel Art (Arcade 3.3.3)

Game clone Flappy Bird pixel art chuẩn mực được xây dựng bằng Python 3.14 và thư viện Python Arcade 3.3.3.

---

## 🌟 Tính năng nổi bật

1. **Chuẩn mực Kiến trúc Arcade 3.3.3**:
   - Sử dụng kiến trúc `arcade.Window` & `arcade.View` (`StartView`, `GameView`, `GameOverView`, `ShopView`).
   - Sử dụng `arcade.camera.Camera2D` khóa viewport ảo $288 \times 512$, hỗ trợ co giãn cửa sổ (`resizable=True`) và chế độ toàn màn hình (`F11`) với tỷ lệ hiển thị nguyên vẹn (Letterboxing/Pillarboxing viền đen).
   - Tận dụng `arcade.Sprite`, `arcade.SpriteList` và các thuật toán kiểm tra va chạm native của Arcade, không tự chế vòng lặp CPU.

2. **Bất biến Hitbox (Hitbox Decoupling)**:
   - Hệ thống skin chấp nhận file ảnh texture bất kỳ kích thước ($32\times32$, $64\times64$, $48\times32$, $1:1$, $2:1$).
   - **Hitbox của chim luôn giữ nguyên kích thước chuẩn ($34 \times 24$ px)** độc lập với kích thước texture ảnh, đảm bảo trải nghiệm chơi công bằng 100%.

3. **Độ khó tăng dần mượt mà (Difficulty Curve with Continuous Lerp)**:
   - Tốc độ cuộn ống tăng dần từ $180 \to 300\text{ px/s}$ và khoảng hở thu hẹp từ $150 \to 110\text{ px}$ theo các mốc điểm ($0, 10, 25, 50+$).
   - Thuật toán nội suy tuyến tính (Lerp) liên tục qua `delta_time`, không nhảy nấc giật cục.

4. **Kinh tế & Hệ thống Mở khóa**:
   - Cứ mỗi 5 điểm ghi được trong ván chơi, người chơi nhận thêm 1 Coin.
   - Mở khóa skin bằng Coin tích lũy hoặc thành tựu (High Score, tổng Coin kiếm được).

5. **Lưu trữ dữ liệu an toàn (Atomic JSON)**:
   - Toàn bộ High Score, Coin, danh sách skin đã mở và skin đang trang bị được lưu tại `data/save_data.json`.
   - Cơ chế ghi file tạm `.tmp` rồi đổi tên (atomic write) chống hỏng file khi tắt game đột ngột.

6. **Tự động sinh Asset (Zero-config Bootstrapping)**:
   - Tự động sinh đầy đủ sprite pixel art và chuẩn bị âm thanh ngay lần chạy đầu tiên mà không cần cài đặt thêm bên ngoài.

---

## 🚀 Hướng dẫn Khởi chạy Game

### Cách 1: Nhanh nhất trên Windows (Khuyên dùng)
Chỉ cần **click đúp vào file `run.bat`** (hoặc chạy trong terminal):
```cmd
run.bat
```
> Script sẽ tự động kiểm tra Python, tạo môi trường ảo `.venv`, cài đặt thư viện cần thiết và khởi chạy game ngay lập tức.

### Cách 2: Chạy trực tiếp từ file `.exe` độc lập (Không cần cài Python)
Nếu bạn đã build hoặc tải bản release, chỉ cần click đúp vào file:
```text
dist/FlappyBird.exe
```
> File chạy độc lập, tự động tích hợp sẵn runtime, đồ họa và âm thanh. File lưu tiến trình (`data/save_data.json`) sẽ tự động được lưu cạnh file `.exe`.

### Cách 3: Tự đóng gói thành file `.exe` (1-Click Build)
Chỉ cần **click đúp vào file `build_exe.bat`**:
```cmd
build_exe.bat
```
> File `.exe` hoàn chỉnh sẽ được tạo tại thư mục `dist/FlappyBird.exe` sẵn sàng gửi cho người chơi khác.

### Cách 4: Khởi chạy thủ công qua dòng lệnh
1. Cài đặt thư viện phụ thuộc:
```bash
pip install -r requirements.txt
```

2. Khởi chạy game:
```bash
python main.py
```

---

## 🎮 Hướng dẫn Điều khiển

| Thao tác | Phím tắt / Chuột |
| :--- | :--- |
| **Nhảy / Vỗ cánh** | Phím `Space`, Mũi tên `Up`, hoặc `Click chuột trái` |
| **Bật/Tắt Toàn màn hình** | `F11` |
| **Vào Shop & Chọn Skin** | Phím `S` (ở màn hình chờ hoặc Game Over), hoặc Click nút `[ SHOP ]` |
| **Duyệt danh sách Skin** | Phím `Left` / `Right` (hoặc `A` / `D`), hoặc Click nút `<` / `>` |
| **Mua / Trang bị Skin** | Phím `Enter`, `Space`, hoặc Click nút hành động |
| **Trở về từ Shop** | Phím `Esc`, `B`, hoặc Click nút `[ ESC ] TRỞ VỀ` |

### 🛠️ Phím tắt Dành cho Lập trình viên (Debug Cheats)
- **`F1`**: Nhận ngay **+10 Coins** (dùng để test mở khóa Shop).
- **`F2`**: Bật/tắt hiển thị **Hitbox viền đỏ ($34 \times 24$)** trực quan trên chim và ống nước.
- **`F3`**: Nhận ngay **+10 Điểm** (dùng để test đường cong độ khó và kỷ lục High Score).
- **`F4`**: Bật/tắt **God Mode (Bất tử)** (chim va chạm không chết, bay test địa hình).

---

## 📁 Cấu trúc Thư mục

```text
FlappyBird/
├── assets/
│   ├── audio/           # Các hiệu ứng âm thanh (.wav)
│   ├── skins/           # Các file texture skin chim (.png)
│   └── sprites/         # Sprite môi trường (background, pipe, base, coin)
├── data/
│   └── save_data.json   # Lưu trữ tiến trình người chơi (tự động tạo)
├── src/
│   ├── constants.py     # Hằng số vật lý, màn hình, kinh tế
│   ├── models/          # Data models (Skin, SaveData)
│   ├── entities/        # Bird (Hitbox chuẩn), Pipe, Floor
│   ├── services/        # StorageService, DifficultyService, SkinManager, AudioService
│   ├── views/           # BaseView, StartView, GameView, GameOverView, ShopView
│   ├── tools/           # generate_placeholders.py
│   └── main.py          # Window & khởi chạy
├── tests/               # 21 unit & E2E tests kiểm tra toàn diện
├── SPEC.md              # Tài liệu đặc tả kỹ thuật
├── requirements.txt
└── README.md
```
