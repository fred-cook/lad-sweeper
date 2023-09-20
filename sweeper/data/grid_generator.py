import numpy as np
from numpy.lib.stride_tricks import as_strided

class GridGenerator:
    """
    A method to generate lad-sweeper grids

    The class can be treated as an iterator, eg. make a
    lad-sweeper grid:
    >>> gen = GridGenerator()
    >>> grid = next(gen)

    However, to make many grids at once call the `generate_n_grids`
    method with the desired number.

    Method
    ------
    1. Generate N sets of shuffled coordinates 1D coordinates.
       Return the first `num_mines` from each set of coordinates
    2. Insert the N coordinates into a 3D pre-made stack of grids
       with a NumPy strided view into it of all the neighbours.
    3. Take the absolute value of the sum of all the neighbours
    4. Put the mines back in place
    """
    def __init__(self, grid_shape=(16, 16), num_mines=44):
        self.grid_shape = grid_shape
        self.rows, self.columns = grid_shape
        self.size = self.rows * self.columns
        self.num_mines = num_mines

        self.rng = np.random.default_rng()

    def __iter__(self):
        return self
    
    def __next__(self):
        return self.generate_n_grids(1)[0]

    def generate_n_grids(self, N: int) -> np.ndarray:
        """
        Generate N lad-sweeper grids

        Parameters
        ----------
        N: int
            The number of grids to make

        Returns
        -------
        grids: np.ndarray
            An array with shape (N, *self,shape)
        """
        # Make a 3D grid padded in the last 2 dimensions to store
        # the mine values
        padded_shape = (N, self.rows + 2, self.columns+2)
        padded = np.zeros(padded_shape, dtype=np.int8)

        # Make N grids with -1 for mines, 0 elsewhere
        mined_grids = self.generate_n_mined_boards(N)
        # Insert them into padded
        padded[:,1:-1,1:-1] = mined_grids

        # Create a strided view of the neighbours of each layer
        strides = (padded.strides[0],) + padded.strides[1:]*2
        new_shape = (N, self.rows, self.columns, 3, 3)
        neighbours = as_strided(padded, new_shape, strides)

        # Sum all of the neighbours over the last 2 axes
        counts = np.abs(np.sum(neighbours, axis=(-1, -2)))

        # Return summed value or mine
        return np.where(mined_grids == -1, -1, counts)

    def generate_n_coords(self, N: int) -> np.ndarray:
        """
        Return N rows of 1D coordinates containing mines

        Parameters
        ----------
        N: int
            Number of rows of mines to generate
        
        Returns
        -------
        mine_coords: np.ndarray
            2D array of 1D mine coordinates with shape
            (N, self.num_mines)
        """
        coords = np.arange(self.size, dtype=np.int8) * np.ones(N, dtype=np.int8)[:,None]
        return self.rng.permuted(coords, axis=1)[:, :self.num_mines]

    def generate_n_mined_boards(self, N: int) -> np.array:
        """
        Return N 2D lad-sweeper boards with mines in place
        but no counts

        Parameters
        ----------
        N: int
            Number of mined boards to make

        Returns
        -------
        mined_grids: np.ndarray
            Grids with mines in place but no counts
        """
        boards = np.zeros((N, self.size), dtype=np.int8)
        rows = np.repeat(np.arange(N), self.num_mines)
        mines = self.generate_n_coords(N)
        boards[(rows.flatten(), mines.flatten())] = -1
        return boards.reshape(N, *self.grid_shape)