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

def send_media_key(vk: int) -> None:
    KEYEVENTF_KEYUP = 0x0002
    try:
        ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
        ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)
        print(f"[OK] Media key {vk} sent")
    except Exception as e:
        print(f"[FAIL] Error sending media key {vk}: {e}")

def run_action(action: str) -> None:
    if not action:
        print("[SKIP] Empty action, skipping.")
        return

    try:
        action = action.lower().strip()
        print(f"[OK] Handling action: {action}")

        match action:
            case "windows+l":
                print("[OK] Locking workstation.")
                ctypes.windll.user32.LockWorkStation()

            case "play/pause media":
                send_media_key(0xB3)

            case "media next":
                send_media_key(0xB0)

            case "media previous":
                send_media_key(0xB1)

            case _:
                print(f"[OK] Sending standard action via keyboard lib: {action}")
                keyboard.send(action)

    except Exception as e:
        print(f"[FAIL] Failed to handle action '{action}': {e}")

def run_prog(path: str) -> None:
    try:
        if path.lower().startswith("url:"):
            url = path[4:].strip()
            print(f"[OK] Opening URL via shell: {url}")
            subprocess.Popen(f'start {url}', shell=True)
        else:
            print(f"[OK] Launching program: {path}")
            subprocess.Popen(path)
        print(f"[OK] Program or URL '{path}' launched successfully.")
    except Exception as e:
        print(f"[FAIL] Failed to launch '{path}': {e}")

def on_press(event) -> None:
    print(f"[OK] Key pressed: {event.name}")
    for item in config:
        if event.name.lower() == item.get("press_key", "").lower():
            print(f"[OK] Matching key found: {item['press_key']}")
            action = item.get("run_action", "")
            prog = item.get("run_prog", "")
            if prog:
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
