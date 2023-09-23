import tkinter as tk
from time import time

from sweeper.gui.three_digit_display import ThreeDigitDisplay

class Clock(ThreeDigitDisplay):
    """
    The timer for a game of lad-sweeper.

    Starts on the first click being made, stops on the
    game being over (win or lose), or the time reaching
    999.

    The clock works by calling the update function
    every `UPDATE_TIME` ms. There may be a better way
    to do it than that.
    """
    UPDATE_TIME = 10 #  [ms]
    def __init__(self, master: tk.Tk):
        super().__init__(master)

        self.stopped = True
        self.start_time: float #  start time from time()

    def start_timer(self):
        if not self.stopped:
            return # clock already running
        self.stopped = False
        self.start_time = time()
        self.value = 0
        self.update_timer()

    def update_timer(self):
        self.value=(int(time()-self.start_time))
        if self.stopped:
            return
        self.master.after(self.UPDATE_TIME, self.update_timer)

    def stop_timer(self):
        self.stopped = True
