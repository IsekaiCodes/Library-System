@echo off
REM BCI Campus Library Management System - Windows Launcher
REM This script starts the application with system checks

setlocal enabledelayedexpansion

color 0A
echo.
echo ████████████████████████████████████████████████████████
echo ██                                                      ██
echo ██  BCI CAMPUS - LIBRARY MANAGEMENT SYSTEM              ██
echo ██                                                      ██
echo ████████████████████████████████████████████████████████
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ✗ ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

REM Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python version: %PYTHON_VERSION%

REM Check for tkinter
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ✗ ERROR: Tkinter is not installed
    echo.
    echo On Windows, tkinter should come with Python
    echo Try reinstalling Python and select "tcl/tk and IDLE"
    echo.
    pause
    exit /b 1
)

echo ✓ Tkinter is available
echo.

REM Check for main.py
if not exist "main.py" (
    color 0C
    echo ✗ ERROR: main.py not found in current directory
    echo.
    echo Make sure you're in the Library-System directory
    echo.
    cd
    echo.
    pause
    exit /b 1
)

echo ✓ All checks passed!
echo.
echo Starting application...
echo.

REM Launch the application
python main.py

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ✗ Application exited with an error
    echo.
    pause
)

exit /b %errorlevel%
