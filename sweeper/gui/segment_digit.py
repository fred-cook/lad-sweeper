import tkinter as tk

import numpy as np

class Digit(tk.Canvas):
    COORDS = np.array([[-25, 0],
                       [-20, 5],
                       [20, 5],
                       [25, 0],
                       [20, -5],
                       [-20, -5]])

    ROT_MAT = np.array([[0, -1], [1, 0]])
    COLOUR = "red"
    NUMBERS = {0: (True, True, True, True, True, True, False),
                1: (False, True, True, False, False, False, False),
                2: (True, True, False, True, True, False, True),
                3: (True, True, True, True, False, False, True),
                4: (False, True, True, False, False, True, True),
                5: (True, False, True, True, False, True, True),
                6: (True, False, True, True, True, True, True),
                7: (True, True, True, False, False, False, False),
                8: (True, True, True, True, True, True, True),
                9: (True, True, True, False, False, True, True),
               "-": (False, False, False, False, False, False, True),
                None: (False,) * 7}
    
    def __init__(self, master: tk.Tk):
        super().__init__(master)
        seg_coords = [[(30, 5), False],
                      [(55, 30), True],
                      [(55, 80), True],
                      [(30, 105), False],
                      [(5, 80), True],
                      [(5, 30), True],
                      [(30, 55), False]]

        for coord, rotated in seg_coords:
            self.make_segment(coord, rotated)
                               

    def make_segment(self, coord: tuple[int, int],
                     rotated: bool=False) -> None:
        if rotated:
            vertices = self.COORDS @ self.ROT_MAT
            print(vertices)
        else:
            vertices = self.COORDS.copy()
        vertices += coord
        self.create_polygon(*vertices.flatten(),
                            fill=self.COLOUR,
                            outline="white")

    def set_value(self, val: int | None) -> None:
        for i, val in enumerate(self.NUMBERS[val], 1):
            if val:
                self.itemconfig(i, fill="red")
            else:
                self.itemconfig(i, fill="gray")
