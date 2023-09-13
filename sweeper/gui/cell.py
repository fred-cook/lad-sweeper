from enum import IntEnum

import tkinter as tk
from tkinter.font import Font


class Cell(tk.Button):
    """
    Stores the style and logic concerning individual cells

    Any images/values to be displayed are passed in, instead
    of holding a reference to the images in every cell
    """
    ZERO_IMAGE = tk.PhotoImage(width=0, height=0)

    COLOURS = {
               0: "white",
               1: "blue",
               2: "green",
               3: "red",
               4: "Purple",
               5: "Maroon",
               6: "Turquoise",
               7: "black",
               8: "gray"}

    UNCLICKED = {
        "text": '',
        "image": ZERO_IMAGE,
        "relief": "raised",
        "state": tk.ACTIVE,
        "compound": "center", #  Will show images and text
        "bg": "white",
    }

    CLICKED = {
        "relief": "solid",
        "state": tk.DISABLED,
    }

    STATES = IntEnum("state", ("UNCLICKED",
                               "CLICKED",
                               "FLAGGED",))

    def __init__(self, master: tk.Tk, size: int, font: Font):
        """
        Parameters
        ----------
        master: tk.Tk
            Owner of the cell
        size: int
            Size of the cell in pixels
        """
        self.size = size #  [pixels]

        super().__init__(master, height=size, width=size, **self.UNCLICKED)
        self.config(font=font)
        self.state = self.STATES.UNCLICKED

    def left_click(self, value: int) -> None:
        """
        Called if a cell is left clicked. Only has effect if the
        cell state is unclicked

        Parameters
        ----------
        value: int
            The value of the cell, with a default of 0
        """
        if self.state is self.STATES.UNCLICKED:
            self.config(text=str(value),
                        fg=self.COLOURS[value],
                        bg="gray")
            self.state = self.STATES.CLICKED

    def right_click(self, flag_image: tk.PhotoImage):
        """
        Called if a cell is right clicked. toggles the state
        between flagged and unclicked

        Parameters
        ----------
        flag_image: tk.PhotoImage
            flag lad image as no images stored in this class
        """
        if self.state is self.STATES.UNCLICKED:
            self.config(image=flag_image)
            self.state = self.STATES.FLAGGED
        elif self.state is self.STATES.FLAGGED:
            self.config(**self.UNCLICKED)
            self.state = self.STATES.UNCLICKED

    def reveal(self, image: tk.PhotoImage, special: bool=False) -> None:
        """
        Reveal the cell on game being won or lost.

        Parameters
        ----------
        image: tk.PhotoImage | None
            Could be lad or bomb
        special: bool
            Used to highlight if it's the mine that triggered
            the loss, or an incorrectly placed flag at the end
        """
        self.config(image=image,
                    **self.CLICKED,
                    bg="red" if special else "gray")
        self.state = self.STATES.CLICKED

    def reset(self):
        self.config(height=self.size, width=self.size, **self.UNCLICKED)
