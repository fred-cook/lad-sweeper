import tkinter as tk
from tkinter import font
from random import randint

colours = {1: "blue",
               2: "green",
               3: "red",
               4: "Purple",
               5: "Maroon",
               6: "Turquoise",
               7: "black",
               8: "gray"}

class Cell:
    def __init__(self, master, coord, callback):
        custom_font = font.Font(family="Minesweeper", size=24)
        self.pixel = tk.PhotoImage(width=1, height=1)
        self.button = tk.Button(master,
                           font=custom_font,
                           image=self.pixel,
                           compound="center",
                           width=40,
                           height=40,
                           text='',
                           command=lambda i=coord[0], j=coord[1]: callback(i, j))
        row, column = coord
        self.button.grid(row=row, column=column)



if __name__ == "__main__":
    root = tk.Tk()

    def callback(i, j):
        val = randint(1, 8)
        b = grid[i][j]
        b.button.config(state=tk.DISABLED, text=str(val))
        b.button.config(width=38, height=38)

    grid = [[None for _ in range(3)] for _ in range(3)]

    for i in range(3):
        for j in range(3):
            grid[i][j] = Cell(root, (i, j), callback)

    root.mainloop()
