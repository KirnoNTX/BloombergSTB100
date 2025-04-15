@echo off
REM Install Python dependencies
pip install keyboard psutil pystray pillow pyinstaller

REM Go to the app directory to compile the script
cd app

REM Compile the Python script into a .exe without console
pyinstaller --onefile --noconsole "BloombergSTB100.py"

REM Return to the root of the project
cd ..

REM Copy the generated executable to the root directory
copy /Y "app\dist\BloombergSTB100.exe" "%~dp0"

REM Delete only PyInstaller generated files from app
rmdir /s /q "app\build"
rmdir /s /q "app\dist"
del /f /q "app\BloombergSTB100.spec"

echo [OK] Build completed successfully (no dangerous deletions).
pause
