from typing import Tuple

import numpy as np
from numpy.lib.stride_tricks import as_strided

class GridGenerator:
    """
    A small class to generate lad sweeper grids.

    Grids are 2d NumPy arrays with -1 denoting a mine
    and a count for the number of adjacent mines.    
    """
    def __init__(self,
                 grid_shape: Tuple[int, int] = (16, 16),
                 num_mines: int = 44):
        """
        Parameters
        ----------
        grid_shape: Tuple[int, int]
            The number of rows and columns which will make up the grid
        num_mines: int
            The number of mines the grid should contain
        """
        self.grid_shape = grid_shape
        self.size = grid_shape[0] * grid_shape[1]
        self.num_mines = min(self.size, num_mines)

        # Set up a padded grid which allows a strided view of every
        # cell's neighbours
        padded_shape = (grid_shape[0] + 2, grid_shape[1] + 2)
        neighbours_shape = (grid_shape[0], grid_shape[1], 3, 3)

        self.padded_grid = np.zeros(padded_shape, dtype=np.int8)
        self.neighbours = as_strided(self.padded_grid,
                                     shape=neighbours_shape,
                                     strides=self.padded_grid.strides * 2)
        
        # Store a list of coords
        self.coords = np.indices(grid_shape).reshape(2, -1).T

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.make_grid()
        
    def make_grid(self) -> np.ndarray:
        """
        Make a grid with the specified shape

        Returns
        -------
        grid: np.ndarray
            A filled grid

        Method
        ------
        1. Shuffle the list of coords and take the first
            `num_mines` from the top
        2. Set those values into an array of zeros as -1
        3. Embed that array into the padded grid
        4. Take the absolute sum of all the neighbours
        5. Reset the mines to -1
        """
        np.random.shuffle(self.coords) #  in place
        board = np.zeros(self.grid_shape, dtype=np.int8)
        board[tuple(self.coords[:self.num_mines].T)] = -1

        self.padded_grid[1:-1, 1:-1] = board
        counts = np.abs(np.sum(self.neighbours, axis=(3, 2)))
        counts[tuple(self.coords[:self.num_mines].T)] = -1 # reset the mines
        return counts
    