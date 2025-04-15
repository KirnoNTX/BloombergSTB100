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
    if not action:
        print("[SKIP] Empty action, skipping.")
        return
    try:
        print(f"[OK] Sending action: {action}")
        keyboard.send(action)
    except Exception as e:
        print(f"[FAIL] Failed to send action '{action}': {e}")

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
        if event.name == item.get("press_key"):
            print(f"[OK] Matching key found: {event['press_key']}")
            action = item.get("run_action", "")
            prog = item.get("run_prog", "")
            
            if prog:
                print(f"[OK] Launching program: {prog}")
                run_prog(prog)
            elif action:
                if item.get("programme_fenêtre_en_cours"):
                    proc = get_proc()
                    if proc and proc.lower() == item["programme_fenêtre_en_cours"].lower():
                        print(f"[OK] Active process match: {proc}")
                        run_action(action)
                    else:
                        print(f"[FAIL] Active process mismatch: {proc} != {item['programme_fenêtre_en_cours']}")
                else:
                    print(f"[OK] Executing action: {action}")
                    run_action(action)
            else:
                print("[SKIP] No action or program defined.")
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
