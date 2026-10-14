@echo off
cd /d "%~dp0"
title Build Flappy Bird Executable (.exe)

echo [1/3] Checking environment and PyInstaller...
if not exist ".venv\Scripts\python.exe" (
    echo ERROR: Virtual environment (.venv) not found.
    echo Please run run.bat first to set up Python and dependencies.
    pause
    exit /b 1
)

.venv\Scripts\python.exe -m pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller.
    pause
    exit /b 1
)

echo [2/3] Ensuring application icon exists...
if not exist "assets\icon.ico" (
    .venv\Scripts\python.exe -c "from PIL import Image; img = Image.open('assets/skins/yellow.png'); img.save('assets/icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64)])"
)

echo [3/3] Packaging standalone FlappyBird.exe...
.venv\Scripts\pyinstaller.exe ^
    --noconfirm ^
    --clean ^
    --onefile ^
    --windowed ^
    --name "FlappyBird" ^
    --icon "assets\icon.ico" ^
    --add-data "assets;assets" ^
    --collect-all arcade ^
    --collect-all pyglet ^
    --collect-all pymunk ^
    main.py

if errorlevel 1 (
    echo.
    echo ERROR: Packaging failed!
    pause
    exit /b 1
)

echo.
echo =========================================================
echo BUILD SUCCESS!
echo File executable: dist\FlappyBird.exe
echo (You can share this single file directly with players)
echo =========================================================
echo.
pause
exit /b 0
