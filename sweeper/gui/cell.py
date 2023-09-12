from pathlib import Path

import tkinter as tk
from tkinter.font import Font

from PIL import Image, ImageTk

class Cell(tk.Button):
    BUTTON_SIZE = 50 # pixels
    FONT = Font(family="Arial Rounded MT Bold", size=20)
    ZERO_IMAGE = tk.PhotoImage(width=0, height=0)

    UNCLICKED = {
        "text": '',
        "font": FONT,
        "image": ZERO_IMAGE,
        "relief": "raised",
        "state": tk.ACTIVE,
        "compound": "center", #  Will show images and text
    }

    CLICKED = {
        "relief": "solid",
        "state": tk.DISABLED,
        "bd": 1,
    }
    def __init__(self, master: tk.Tk, size: int):
        super().__init__(self, height=size, width=size, **self.UNCLICKED)