@echo off
cd /d "%~dp0"
title Flappy Bird

echo [1/3] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python is not installed or not in PATH.
    echo Please download and install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [2/3] Checking dependencies...
if exist ".venv\Scripts\python.exe" goto install_deps

echo Creating virtual environment .venv...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

:install_deps
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements.
    pause
    exit /b 1
)

echo [3/3] Launching Flappy Bird...
.venv\Scripts\python.exe main.py
if errorlevel 1 (
    echo.
    echo Game exited with an error.
    pause
    exit /b 1
)

exit /b 0
