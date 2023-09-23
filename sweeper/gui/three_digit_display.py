import tkinter as tk

from sweeper.gui.segment_digit import Digit

class ThreeDigitDisplay(tk.Frame):
    """
    Display values between -99 and 999 on a 7seg display
    """
    def __init__(self, master):
        super().__init__(master, bg="black", bd=0)
        self.digits = [Digit(self) for _ in range(3)]
        for i, digit in enumerate(self.digits):
            digit.grid(row=0, column=i, padx=0, pady=0, ipadx=0, ipady=0)
        
        self.value = 0

    @property
    def value(self) -> int:
        return int(self._value)

    @value.setter
    def value(self, value: int) -> None:
        self._value = f"{max(-99, min(value, 999)):03d}"
        for digit, char in zip(self.digits, self._value):
            digit.set_value(char)
