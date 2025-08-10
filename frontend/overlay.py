import threading
import pygetwindow as gw
import tkinter as tk
import win32gui
from PIL import ImageGrab
import requests


TARGET_WINDOW_TITLE = "Isaac"
BACKEND_URL = "http://localhost:8080/api/items/identify"


def is_target_window_focused(target_title):
    try:
        active_hwnd = win32gui.GetForegroundWindow()
        target_hwnd = win32gui.FindWindow(None, target_title)
        return active_hwnd == target_hwnd
    except:
        return False


def get_window_rect(title):
    try:
        window = gw.getWindowsWithTitle(title)[0]
        return {
            "top": window.top,
            "left": window.left,
            "width": window.width,
            "height": window.height
        }
    except IndexError:
        return None


overlay = tk.Tk()
overlay.attributes("-topmost", True)
overlay.attributes("-transparentcolor", "white")
overlay.overrideredirect(True)
overlay.config(bg="white")

label = tk.Label(overlay, text="Overlay active", font=("Arial", 20), bg="white", fg="red")
label.pack()


def update_overlay():
    print("Updating overlay...")
    rect = get_window_rect(TARGET_WINDOW_TITLE)
    focused = is_target_window_focused(TARGET_WINDOW_TITLE)

    if rect and focused:
        screenshot_path = capture_window()
        if screenshot_path:
            send_screenshot_async(screenshot_path)

        x, y = rect["left"], rect["top"]
        w, h = rect["width"], rect["height"]
        overlay.geometry(f"{w}x40+{x}+{y}")
        overlay.deiconify()
    else:
        overlay.withdraw()

    overlay.after(1000, update_overlay)


def capture_window():
    rect = get_window_rect(TARGET_WINDOW_TITLE)
    focused = is_target_window_focused(TARGET_WINDOW_TITLE)
    if rect and focused:
        bbox = (
            rect["left"],
            rect["top"],
            rect["left"] + rect["width"],
            rect["top"] + rect["height"]
        )
        img = ImageGrab.grab(bbox)
        img.save("screenshot.png")
        return "screenshot.png"
    return None


def send_screenshot(path):
    with open(path, "rb") as f:
        files = {"file": (path, f, "image/png")}
        try:
            r = requests.post(BACKEND_URL, files=files)
            r.raise_for_status()
            return r.text
        except requests.RequestException as e:
            print(f"Error sending screenshot: {e}")
            return "Error contacting backend"


def send_screenshot_async(path):
    def task():
        result = send_screenshot(path)
        overlay.after(0, lambda: label.config(text=result))
    threading.Thread(target=task, daemon=True).start()


update_overlay()
overlay.mainloop()
