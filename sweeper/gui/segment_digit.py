import tkinter as tk

import numpy as np

class Digit(tk.Canvas):
    r"""
    7seg digit

    Each segment has shape:
            _________
           /         \
           \_________/
    Their centre is defined as (0, 0), with half width/height
    taken to the extremes from there. Width and height are
    defined in this horizontal lay out

    Segments are then numbered clockwise from the top, with
    the centre seg the last value.
    """
    HALF_HEIGHT = 5 #  [px]
    HALF_WIDTH = 25 #  [px]
    HEIGHT = HALF_HEIGHT * 2
    WIDTH = HALF_WIDTH * 2
    POLYGON_COORDS = np.array([[-(HALF_WIDTH), 0],
                               [-(HALF_WIDTH-HALF_HEIGHT), HALF_HEIGHT],
                               [(HALF_WIDTH-HALF_HEIGHT), HALF_HEIGHT],
                               [HALF_WIDTH, 0],
                               [(HALF_WIDTH-HALF_HEIGHT), -HALF_HEIGHT],
                               [-(HALF_WIDTH-HALF_HEIGHT), -HALF_HEIGHT]])
    ROT_MAT = np.array([[0, -1], [1, 0]])
    ON_COLOUR = "#d60000"
    OFF_COLOUR = "#783030"
    PADDING = 4 #  [px]
    BG = "black"
    NUMBERS = {'0': (True, True, True, True, True, True, False),
               '1': (False, True, True, False, False, False, False),
               '2': (True, True, False, True, True, False, True),
               '3': (True, True, True, True, False, False, True),
               '4': (False, True, True, False, False, True, True),
               '5': (True, False, True, True, False, True, True),
               '6': (True, False, True, True, True, True, True),
               '7': (True, True, True, False, False, False, False),
               '8': (True, True, True, True, True, True, True),
               '9': (True, True, True, False, False, True, True),
               "-": (False, False, False, False, False, False, True),
               None: (False,) * 7}
    
    def __init__(self, master: tk.Tk):
        super().__init__(master,
                         width=self.HEIGHT + self.WIDTH + self.PADDING,
                         height=2 * (self.HEIGHT + self.WIDTH),
                         bg=self.BG)

        seg_x_coords = (self.HALF_WIDTH + self.HALF_HEIGHT,  #  top seg
                        self.WIDTH + self.HALF_HEIGHT,
                        self.WIDTH + self.HALF_HEIGHT,
                        self.HALF_WIDTH + self.HALF_HEIGHT,  #  bottom seg
                        self.HALF_HEIGHT,
                        self.HALF_HEIGHT,
                        self.HALF_WIDTH + self.HALF_HEIGHT)  #  middle seg

        seg_y_coords = (self.HEIGHT,
                        self.HALF_WIDTH + self.HEIGHT,
                        self.WIDTH + self.HALF_WIDTH + self.HEIGHT,
                        self.WIDTH + self.WIDTH + self.HEIGHT,
                        self.WIDTH + self.HALF_WIDTH + self.HEIGHT,
                        self.HALF_WIDTH + self.HEIGHT,
                        self.HEIGHT + self.WIDTH)

        rotated = (False, True, True, False, True, True, False)

        for x, y, rotated in zip(seg_x_coords, seg_y_coords, rotated):
            self.make_segment((x, y), rotated)                            

    def make_segment(self, coord: tuple[int, int],
                     rotated: bool=False) -> None:
        """
        Draw the segments on the canvas. They can be accessed
        by integer order of drawing starting at 1
        """
        if rotated:
            vertices = self.POLYGON_COORDS @ self.ROT_MAT
        else:
            vertices = self.POLYGON_COORDS.copy()
        vertices += coord
        vertices[:,0] += self.PADDING
        self.create_polygon(*vertices.flatten(),
                            fill=self.OFF_COLOUR,
                            outline=self.BG,
                            width=2)

    def set_value(self, val: str | None) -> None:
        """
        Set the display to val

        valid values for val:
            - [0-9]
            - '-'
            - None
        Otherwise it defaults to None
        """
        for i, val in enumerate(self.NUMBERS.get(val, self.NUMBERS[None]), 1):
            if val:
                self.itemconfig(i, fill=self.ON_COLOUR)
            else:
                self.itemconfig(i, fill=self.OFF_COLOUR)
