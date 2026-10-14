@echo off
cd /d "%~dp0"
title Build Flappy Bird Executable (.exe)

echo =========================================================
echo       FLAPPY BIRD - EXE PACKAGING TOOL
echo =========================================================
echo.

echo [1/3] Kiem tra moi truong .venv va PyInstaller...
if not exist ".venv\Scripts\python.exe" (
    echo.
    echo LOI: Khong tim thay moi truong ao .venv!
    echo Vui long chay run.bat truoc de tao moi truong.
    echo.
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m pip install pyinstaller
if errorlevel 1 (
    echo.
    echo LOI: Cai dat PyInstaller that bai.
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] Kiem tra icon ung dung...
if not exist "assets\icon.ico" (
    .venv\Scripts\python.exe -c "from PIL import Image; img = Image.open('assets/skins/yellow.png'); img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])"
)

echo.
echo [3/3] Dang dong goi FlappyBird.exe bang PyInstaller...
echo Qua trinh nay mat khoang 1-2 phut, vui long cho...
echo.

.venv\Scripts\pyinstaller.exe --noconfirm --clean --onefile --windowed --name "FlappyBird" --icon "assets\icon.ico" --add-data "assets;assets" --collect-all arcade --collect-all pyglet --collect-all pymunk main.py

if errorlevel 1 (
    echo.
    echo LOI: Dong goi that bai!
    echo.
    pause
    exit /b 1
)

echo.
echo =========================================================
echo DONG GOI THANH CONG!
echo File chay da duoc tao tai: dist\FlappyBird.exe
echo (Ban co the gui truc tiep file nay cho nguoi choi)
echo =========================================================
echo.
pause
exit /b 0