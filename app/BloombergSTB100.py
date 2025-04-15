import keyboard
import psutil
import json
import ctypes
import os
import sys
import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

def get_proc() -> str | None:
    try:
        print("[OK] Trying to get the active window process...")
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        pid = ctypes.wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        process = psutil.Process(pid.value)
        print(f"[OK] Active process: {process.name()}")
        return process.name()
    except Exception as e:
        print(f"[FAIL] Failed to get process name: {e}")
        return None

def config_path() -> str:
    path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    return os.path.join(path, 'config.json')

def load_cfg() -> list:
    path = config_path()
    print(f"[OK] Loading config from {path}...")
    if not os.path.exists(path):
        print("[FAIL] Config file does not exist.")
        return []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
            print("[OK] Config loaded successfully.")
            return cfg
    except json.JSONDecodeError as e:
        print(f"[FAIL] Failed to load config file: {e}")
        return []

def run_action(action: str) -> None:
    try:
        print(f"[OK] Executing action: {action}")
        keyboard.press_and_release(action)
    except ValueError:
        print(f"[FAIL] Invalid key, writing text instead: {action}")
        keyboard.write(action)

def run_prog(path: str) -> None:
    try:
        print(f"[OK] Launching program: {path}")
        subprocess.Popen(path)
        print(f"[OK] Program '{path}' launched successfully.")
    except Exception as e:
        print(f"[FAIL] Failed to launch program '{path}': {e}")

def on_press(event) -> None:
    print(f"[OK] Key pressed: {event.name}")
    for item in config:
        print(f"[OK] Checking config: {item}")
        if event.name == item['press_key']:
            print(f"[OK] Matching key found: {item['press_key']}")
            if 'run_prog' in item:
                print(f"[OK] Launching specified program: {item['run_prog']}")
                run_prog(item['run_prog'])
            elif 'run_action' in item:
                if 'programme_fenêtre_en_cours' in item:
                    proc = get_proc()
                    if proc and proc.lower() == item['programme_fenêtre_en_cours'].lower():
                        print(f"[OK] Active process match: {item['programme_fenêtre_en_cours']}")
                        run_action(item['run_action'])
                    else:
                        print(f"[FAIL] Active process mismatch: {proc} != {item['programme_fenêtre_en_cours']}")
                else:
                    print("[OK] No specific process required, executing action...")
                    run_action(item['run_action'])
            break

def tray_img(w: int, h: int, c1: str, c2: str) -> Image.Image:
    print("[OK] Creating tray icon image...")
    img = Image.new('RGB', (w, h), c1)
    dc = ImageDraw.Draw(img)
    dc.rectangle((w // 4, h // 4, w * 3 // 4, h * 3 // 4), fill=c2)
    print("[OK] Tray icon image created.")
    return img

def quit_app(icon, item) -> None:
    print("[OK] Exiting application from tray icon...")
    icon.stop()

def icon_path() -> str:
    path = os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__))
    return os.path.join(path, 'icon.png')

def tray() -> None:
    print("[OK] Initializing tray icon...")
    path = icon_path()
    if not os.path.exists(path):
        print(f"[FAIL] Icon '{path}' does not exist. Check path.")
        return
    img = Image.open(path)
    menu = Menu(MenuItem('Exit STB100 Companion', quit_app))
    icon = Icon("STB100 Companion", img, "STB100 Companion", menu)
    print("[OK] Tray icon configured and running.")
    icon.run()

config: list = load_cfg()
keyboard.on_press(on_press)
print("[OK] Listening for key presses. Press 'esc' to quit.")
tray()
