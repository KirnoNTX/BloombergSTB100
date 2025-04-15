@echo off
REM Install required packages
pip install keyboard psutil pystray pillow pyinstaller

REM Build the .exe without console
pyinstaller --onefile --noconsole "BloombergSTB100.py"

REM Copy the built .exe to root (already done by default, since no subfolder)
copy /Y "dist\BloombergSTB100.exe" "%~dp0"

REM Clean up PyInstaller build artifacts
rmdir /s /q "build"
rmdir /s /q "dist"
del /f /q "BloombergSTB100.spec"

echo [OK] Build complete.
pause
