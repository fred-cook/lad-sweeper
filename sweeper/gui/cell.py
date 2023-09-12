from pathlib import Path

import tkinter as tk
from tkinter.font import Font

from PIL import Image, ImageTk

class Cell(tk.Button):
    def __init__(self, master: tk.Tk, coords: tuple[int, int]):
        pass