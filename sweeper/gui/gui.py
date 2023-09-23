from typing import Tuple, List

from pathlib import Path
import tkinter as tk
from tkinter.font import Font

from PIL import Image, ImageTk

import numpy as np

from sweeper.lad_sweeper import LadSweeper

from sweeper.gui.image_handler import ImageHandler
from sweeper.gui.cell import Cell


class LadSweeperApp():

    CELL_SIZE = 50 # pixels

    def __init__(self,
                 master: tk.Tk,
                 shape: Tuple[int, int]=(16, 30),
                 num_mines: int=99):
        self.master = master
        master.title("LadSweeper")

        self.shape = shape
        self.num_mines = num_mines
        self.game = LadSweeper(shape=shape, num_mines=num_mines)
        self.images = ImageHandler(self.CELL_SIZE)

        self.new_game_button: tk.Button
        self.banner = self.make_banner(master)
        self.banner.pack(side=tk.TOP)

        self.buttons_frame = tk.Frame(master)
        self.buttons  = self.make_buttons(self.buttons_frame, *shape)
        self.buttons_frame.pack(side=tk.BOTTOM)
        self.flags: List[Tuple[int, int]]=[]


    def make_banner(self, master):
        banner = tk.Frame(master)
        self.new_game_button = tk.Button(banner,
                                      image=self.images["lad"],
                                      height=self.CELL_SIZE,
                                      width=self.CELL_SIZE,
                                      command=self.new_game)
        self.new_game_button.pack()
        return banner

    def new_game(self):
        self.game.new_game()
        self.reset_buttons()
        self.flags = []
        self.new_game_button.config(image=self.images["lad"])

    def reset_buttons(self):
        for row in self.buttons:
            for button in row:
                button.reset()

    def make_buttons(self, master, rows, columns) -> List[List[tk.Button]]:
        buttons = [[] for _  in range(rows)]
        
        for i in range(rows):
            for j in range(columns):
                button = Cell(master=master, size=self.CELL_SIZE)
                buttons[i].append(button)
                buttons[i][j].bind("<Button-1>", lambda _, coord=(i, j): self.on_click(coord))
                buttons[i][j].bind("<Button-3>", lambda _, coord=(i, j): self.on_right_click(coord))
                buttons[i][j].grid(row=i, column=j, padx=1, pady=1)
        return buttons

    def on_click(self, coord: Tuple[int, int]):
        if self.buttons[coord[0]][coord[1]].state is self.buttons[0][0].STATES.CLICKED:
            return
        for i, j in self.game.click_cell(coord):
            value = self.game.board[i, j]
            self.buttons[i][j].left_click(value)
        if self.game.game_won is not None:
            self.reveal_board(coord) # need the coord incase it was a mine
        
    def on_right_click(self, coord):
        """
        Toggle a flag on the cell
        """
        i, j = coord
        if coord in self.flags:
            self.buttons[i][j].right_click(self.images["flag"])
            self.flags.remove(coord)
        elif self.buttons[i][j].state is self.buttons[i][j].STATES.UNCLICKED:
            self.buttons[i][j].right_click(self.images["flag"])
            self.flags.append(coord)

    def reveal_board(self, coord: Tuple[int, int]):
        """
        On the game being won / lost reveal the board
        """
        if self.game.game_won is True:
            self.new_game_button.config(image=self.images["winning_lad"])
            img = self.images["lad"]
        else:
            self.new_game_button.config(image=self.images["lad_rear"])
            img = self.images["dead_lad"]
        for i, row in enumerate(self.buttons):
            for j, button in enumerate(row):
                value = self.game.board[i][j]
                button.disable()
                if value < 0:
                    if (i, j) in self.flags:
                        continue
                    if (i, j) == coord: # losing mine
                        button.reveal(img, special=True)
                    else:
                        button.reveal(img)
                elif (i, j) in self.flags: # incorrect flag
                    button.reveal(self.images["flag"], special=True)
                else: # Don't change, but do disable
                    button.reveal() # just disables


if __name__ == "__main__":
    root = tk.Tk()
    app = LadSweeperApp(root, (10, 10), 15)
    print(app.game._board)
    root.mainloop()
