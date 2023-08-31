from typing import Union, Tuple, Set, List
from itertools import product

import numpy as np

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
        :shape: tuple of ints giving the board shape (rows, columns)
        :num_mines: int for the number of mines to put in the grid
        """
        self.shape = shape
        self.num_mines = num_mines # could error check this
        self.size = shape[0] * shape[1]

        # None if game in progress, True if win, False if lost
        self.game_won: Union[None, bool]

        self._board: np.ndarray
        self.visible: np.ndarray

        self.new_game()

    def new_game(self) -> None:
        self._board = self.create_board()
        self.visible = np.zeros(self.shape, dtype=np.int8)
        self.game_won = None

    def create_board(self) -> np.ndarray:
        """
        Create a new board, with random mine placements and
        numbers for the non-mine cells
        """
        board = np.zeros(self.shape, dtype=np.int8)
        board[self.random_mine_coords()] = -1
        counts = [[np.abs(np.sum(board[self.get_neighbours_np((i, j))]))
                   for j in range(len(row))]
                   for i, row in enumerate(board)]
        return np.where(board < 0, board, counts)

    def random_mine_coords(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Return a list of coords for mines to be placed by
        shuffling a 1d list of integers 0 -> self.size and
        ravelling them back to 2d coordinates
        """
        all_coords = np.arange(self.size)
        np.random.shuffle(all_coords)
        mines = all_coords[:self.num_mines]
        return (mines // self.shape[1], mines % self.shape[1])

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
        result = self.reveal_cell(coord)
        print(len(result))
        if self.check_win():
            self.game_won = True
        if len(result) == 0: # Gameover
            self.game_won = False
            self.visible[:, :] = 1
        return result

    def reveal_cell(self,
                   coord: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Update self._visible to reveal the cell.
        
        if the cell is 0 recursively reveal the board until
        all linked 0 cells are revealed.

        Parameters
        ----------
        coord: Tuple[int, int]
            (row, column) co-ordinate of the cell to click

        Returns
        -------
        Set[Tuple[int, int]]
            A list of board co-ordinates to reveal
            If a mine is clicked the list is empty
        """
        return self.recurse(coord)

    def recurse(self, coord: Tuple[int, int],
                found=None) -> Set[Tuple[int, int]]:
        """
        Recursively reveal cells around a clicked cell.
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
