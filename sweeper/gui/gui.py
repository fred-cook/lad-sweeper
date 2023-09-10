from typing import Tuple, List

from pathlib import Path
import tkinter as tk
from tkinter.font import Font

from PIL import Image, ImageTk

import numpy as np

from sweeper.lad_sweeper import LadSweeper


root = tk.Tk()


class LadSweeperApp():

    BUTTON_SIZE = 50 # pixels
    FONT = Font(family="Arial Rounded MT Bold", size=20)
    ZERO_IMAGE = tk.PhotoImage(width=0, height=0)

    colours = {1: "blue",
               2: "green",
               3: "red",
               4: "Purple",
               5: "Maroon",
               6: "Turquoise",
               7: "black",
               8: "gray"}
    
    UNCLICKED = {
        "text": '',
        "font": FONT,
        "image": tk.PhotoImage(width=0, height=0),
        "relief": "raised",
        #"bg": "#f2cd7e",
        "state": tk.ACTIVE,
        "compound": "center",
        "height": BUTTON_SIZE,
        "width": BUTTON_SIZE,
    }

    CLICKED = {
        "relief": "solid",
        #"bg": "#fcfbf7",
        "state": tk.DISABLED,
        "width": BUTTON_SIZE - 2,
        "height": BUTTON_SIZE - 2,
        "bd": 1,
    }

    def __init__(self,
                 master: tk.Tk,
                 shape: Tuple[int, int]=(16, 30),
                 num_mines: int=99):
        self.master = master
        master.title("LadSweeper")

        self.shape = shape
        self.num_mines = num_mines
        self.game = LadSweeper(shape=shape, num_mines=num_mines)
        self.images = self.get_images()

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
                                      height=self.BUTTON_SIZE,
                                      width=self.BUTTON_SIZE,
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
                button.config(**self.UNCLICKED)

    def get_images(self):
        image_root = Path("sweeper/images")
        images = [Image.open(path) for path in image_root.iterdir()]
        names = [path.stem for path in image_root.iterdir()]
        images = [img.resize((self.BUTTON_SIZE-2, self.BUTTON_SIZE-2))
                  for img in images]
        images = {name: ImageTk.PhotoImage(img)
                  for name, img in zip(names, images)}
        return images


    def make_buttons(self, master, rows, columns) -> List[List[tk.Button]]:
        buttons = [[] for _  in range(rows)]
        
        for i in range(rows):
            for j in range(columns):
                button = tk.Button(master=master, **self.UNCLICKED)
                buttons[i].append(button)
                buttons[i][j].bind("<Button-1>", lambda _, coord=(i, j): self.on_click(coord))
                buttons[i][j].bind("<Button-3>", lambda _, coord=(i, j): self.on_right_click(coord))
                buttons[i][j].grid(row=i, column=j, padx=1, pady=1)
        return buttons

    def on_click(self, coord: Tuple[int, int]):
        if (self.game.game_won is False or
            self.buttons[coord[0]][coord[1]].cget("relief") == "solid" or
            coord in self.flags):
            return

        for i, j in self.game.click_cell(coord):
            value = self.game.board[i, j]
            if value:
                self.buttons[i][j].config(text=str(value),
                                          fg=self.colours[value])
            self.buttons[i][j].config(**self.CLICKED)
        if self.game.game_won is not None:
            self.reveal_board(coord) # need the coord incase it was a mine
        
    def on_right_click(self, coord):
        """
        Toggle a flag on the cell
        """
        i, j = coord
        if self.game.visible[coord]:
            return
        if coord in self.flags:
            self.buttons[i][j].config(image=self.ZERO_IMAGE)
            self.flags.remove(coord)
        else:
            self.buttons[i][j].config(image=self.images["flag"])
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
                if value < 0:
                    if (i, j) in self.flags:
                        continue
                    button.config(image=img,
                                  relief="solid")
                elif (i, j) in self.flags:
                    button.config(image=self.images["incorrect_flag"])
                else:
                    self.on_click((i, j))
        if self.game.game_won is False:
            self.buttons[coord[0]][coord[1]].config(image=self.images["losing_lad"])


if __name__ == "__main__":
    app = LadSweeperApp(root, (10, 10), 15)
    print(app.game._board)
    root.mainloop()
