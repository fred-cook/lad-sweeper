import tkinter as tk

from sweeper.gui.three_digit_display import ThreeDigitDisplay

class MineCounter(ThreeDigitDisplay):
    def __init__(self, master: tk.Tk, count: int):
        super().__init__(master)
        self.value = count

    def raise_count(self) -> None:
        """Add 1 to the count"""
        self.value += 1

    def lower_count(self) -> None:
        """Take 1 away from the count"""
        self.value -= 1
