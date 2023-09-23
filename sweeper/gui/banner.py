import tkinter as tk

from sweeper.gui.clock import Clock
from sweeper.gui.mine_counter import MineCounter


class Banner(tk.Frame):
    def __init__(self, master: tk.Tk,
                 mine_count: int, image: tk.PhotoImage):
        super().__init__(master)
        
        self.clock = Clock(self)
        self.clock.grid(row=0, column=2, sticky="E")

        self.mine_counter = MineCounter(self, mine_count)
        self.mine_counter.grid(row=0, column=0, sticky="W")

        self.new_game_button = tk.Button(self, image=image)
        self.new_game_button.grid(row=0, column=1)
