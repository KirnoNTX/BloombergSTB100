@echo off
title BloombergSTB100 Companion Launcher
color 0B

echo "========================================================================"
echo "    ____     __                              __                         "
echo "   / __ )   / /  ____   ____    ____ ___    / /_   ___    _____   ____ _"
echo "  / __  |  / /  / __ \ / __ \  / __ `__ \  / __ \ / _ \  / ___/  / __ `/"
echo " / /_/ /  / /  / /_/ // /_/ / / / / / / / / /_/ //  __/ / /     / /_/ / "
echo "/_____/  /_/   \____/ \____/ /_/ /_/ /_/ /_.___/ \___/ /_/      \__, /  "
echo "                                                               /____/   "
echo "                   BloombergSTB100 Companion Launcher                   "
echo "                          Powered by Natyx.net                          "
echo "========================================================================"
echo .
echo 1. Build the application (create BloombergSTB100.exe)
echo 2. Add BloombergSTB100 to startup
echo 3. Remove BloombergSTB100 from startup
echo .
set /p choice=Enter your choice [1/2/3]:

IF "%choice%"=="1" GOTO build
IF "%choice%"=="2" GOTO add_startup
IF "%choice%"=="3" GOTO remove_startup
GOTO end

:build
echo [OK] Installing dependencies...
pip install keyboard psutil pystray pillow pyinstaller

echo [OK] Building executable...
pyinstaller --onefile --noconsole "BloombergSTB100.py"

echo [OK] Copying executable to root...
copy /Y "dist\BloombergSTB100.exe" "%~dp0"

echo [OK] Cleaning up...
rmdir /s /q "build"
rmdir /s /q "dist"
del /f /q "BloombergSTB100.spec"

echo [OK] Build completed successfully.
pause
GOTO end

:add_startup
echo [OK] Adding BloombergSTB100 to startup...
set SHORTCUT="%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\BloombergSTB100.lnk"
powershell -Command "$s = (New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%~dp0BloombergSTB100.exe'; $s.Save()"
echo [OK] Added to startup.
pause
GOTO end

:remove_startup
echo [OK] Removing BloombergSTB100 from startup...
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\BloombergSTB100.lnk"
echo [OK] Removed from startup.
pause
GOTO end

:end
exit
