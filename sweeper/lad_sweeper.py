from typing import Union, Tuple, Set, List
from itertools import product

import numpy as np

from sweeper.data.grid_generator import GridGenerator

class LadSweeper:
    """
    I've crammed minesweeper into this class. Could probably
    be split into a few but whatevs.
    """
    MAX_BOARD_SIZE = 50
    NEIGHBOURS = [(i, j) for i, j in product(*((1, 0, -1),)*2)
                  if not (i == j == 0)] #  lmao

    def __init__(self,
                 shape: Tuple[int, int]=(16, 32),
                 num_mines: int=99):
        """
        The default values are for 'expert' lad sweeper

        Parameters
        ----------
        shape: tuple[int, int]
            Lad-sweeper grid shape
        num_mines: int
            Number of mines to place in the lad-sweeper grid
        """
        self._shape = shape
        self._num_mines = num_mines

        self.shape = shape
        self.num_mines = num_mines

        self.grid_generator = GridGenerator(grid_shape=shape, num_mines=num_mines)

        # None if game in progress, True if win, False if lost
        self.game_won: bool | None = None

        self._board: np.ndarray
        self.visible: np.ndarray

        self.new_game()

    @property
    def shape(self) -> tuple[int, int]:
        return self._shape
    
    @shape.setter
    def shape(self, value: tuple[int, int]):
        self._shape = value
        self._size = value[0] * value[1]
        self.grid_generator = GridGenerator(grid_shape=self.shape,
                                            num_mines=self.num_mines)

    @property
    def size(self) -> int:
        return self._size
    
    @property
    def num_mines(self) -> int:
        return self._num_mines
    
    @num_mines.setter
    def num_mines(self, value: int):
        self._num_mines = min(1, max(value, self.size))
        self.grid_generator = GridGenerator(grid_shape=self.shape,
                                            num_mines=self.num_mines)

    def new_game(self) -> None:
        self._board = next(self.grid_generator)
        self.visible = np.zeros(self.shape, dtype=np.int8)
        self.game_won = None

    def get_neighbours(self,
                       coord: Tuple[int, int]) -> Tuple[Tuple[int, int]]:
        """
        Given a cell coordinate as input return a list of valid
        neighbouring coordinates. Returned in format for
        fancy indexing
        """
        row, column = coord
        neighbours = [(row + i, column + j) for i, j in self.NEIGHBOURS
                      if self.valid_coordinate(row + i, column + j)]
        return neighbours

    def get_neighbours_np(self,
                          coord: Tuple[int, int]) -> Tuple[Tuple[int, int]]:
        """
        Return neighbours in a format that can be fancy indexed
        straight into a numpy array
        """
        return tuple(zip(*self.get_neighbours(coord)))

    def valid_coordinate(self, i: int, j: int):
        """
        For row i and column j
        Return True if the coordinate is on self._board, else False
        """
        if (0 <= i < self.shape[0]) and (0 <= j < self.shape[1]):
            return True
        return False

    def click_cell(self,
                   coord: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Pass on a cell coordinate to the board.

        Update the gamestate corresponding to the
        value of the revealed cell.
        """
        result = self.recurse(coord)
        if self.check_win():
            self.game_won = True
        if len(result) == 0: # Gameover
            self.game_won = False
            self.visible[:, :] = 1
        return result

    def recurse(self, coord: Tuple[int, int],
                found: set[Tuple[int, int]] | None=None) -> Set[Tuple[int, int]]:
        """
        Recursively reveal cells around a clicked cell.

        Returns
        -------
        coords: set[Tuple[int, int]]
            - empty if game over (mine was clicked)
            - single tuple for a number clicked
            - several tuples if a 0 was clicked
        """
        if self._board[coord] < 0:
            return set() # Game over
        if found is None:
            found = set()
        if self.visible[coord]:
            return found.union({coord})
        if not self.visible[coord]:
            self.visible[coord] = 1
            found.add(coord)
            if self._board[coord] != 0:
                return found
            else:
                for neib in self.get_neighbours(coord):
                    if neib not in found:
                        found = found.union(self.recurse(neib, found))
        return found

    def check_win(self) -> bool:
        """
        Check if the game has been won.

        Returns
        -------
        True if game is won, else false
        """
        unseen = self._board[np.where(self.visible==0)]
        if np.all(unseen < 0):
            self.visible[:, :] = 1
            return True
        else:
            return False

    @property
    def board(self):
        return np.where(self.visible, self._board, 0)

if __name__ == "__main__":
    game = LadSweeper((10, 10), 15)
