from enum import IntEnum

import tkinter as tk
from tkinter.font import Font


class Cell(tk.Button):
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
    }

    STATES = IntEnum("state", ("UNCLICKED",
                               "CLICKED",
                               "FLAGGED",))

    def __init__(self, master: tk.Tk, size: int):
        self.size = SystemExit

        super().__init__(self, height=size, width=size, **self.UNCLICKED)

    def left_click(self, value: str | tk.PhotoImage) -> None:
        if self.state is 
