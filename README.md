# BloombergSTB100 Companion

![BloombergSTB100 Companion](icon.png)

**BloombergSTB100 Companion** is a background tool designed to work with Bloomberg STB100-style programmable keyboards. It lets you map custom keys to apps, URLs, media controls, and OS-level actions.

---

## 🎹 Function Key Mappings

| Key     | Action                                |
|---------|----------------------------------------|
| F13     | Launch [Everything](https://www.voidtools.com) Search |
| F14     | Media: Previous Track                  |
| F15     | Open [Status](https://status.2222.ovh) page |
| F16     | Launch Visual Studio Code              |
| F17     | Open [Proxmox](https://pve.2222.ovh) |
| F18     | Media: Play / Pause                    |
| F19     | Simulate `Windows + Shift + T`         |
| F20     | Simulate `Windows + Shift + C`         |
| F21     | Open [nMail](https://nmail.natyx.net) |
| F22     | Media: Next Track                      |
| F23     | Open [nPanel](https://npanel.natyx.net) |
| F24     | Open [Natyx.net](https://natyx.net) |
| Pause   | Lock your computer (`Windows + L`)     |

---

## ⚙️ Installation

1. Clone the repo or download the latest release.
2. Verify that the `config.json` file matches your personal key mappings and usage needs.  
   You can edit it to assign each function key to an app, URL, media control, or system shortcut.  
   Example mappings include launching programs, locking the screen, or opening browser tabs.
3. Run `start.bat`.
    The batch script will show a simple menu:
    - Then press `1` to build the app.
    - Press `2` if you want BloombergSTB100 to launch automatically at Windows startup.
    - Press `3` if you wish to suppress the automatic launch at Windows startup.
4. Once the build is complete, launch `BloombergSTB100.exe`.
5. You’re done! You can either:
    - Run the `.exe` manually
    - Or reboot your PC if you chose the startup option

The app will appear in the system tray and listen for your custom key mappings in the background.

## 📈 Usage

RAM : 23,5MB
CPU : Like 0%
