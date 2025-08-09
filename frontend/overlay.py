import pygetwindow as gw
import tkinter as tk
import win32gui
from PIL import ImageGrab


TARGET_WINDOW_TITLE = "Isaac"


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
    rect = get_window_rect(TARGET_WINDOW_TITLE)
    focused = is_target_window_focused(TARGET_WINDOW_TITLE)

    if rect and focused:
        x, y = rect["left"], rect["top"]
        w, h = rect["width"], rect["height"]
        overlay.geometry(f"{w}x40+{x}+{y}")
        overlay.deiconify()
    else:
        overlay.withdraw()

    overlay.after(100, update_overlay)
    overlay.after(1000, lambda: capture_window("Isaac"))


def capture_window(title):
    rect = get_window_rect(title)
    if rect:
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


update_overlay()
overlay.mainloop()
