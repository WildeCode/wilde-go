# WildeStone.py  An open-source Go engine that uses the GPT2 protocol.
#
#    Copyright (C) 2023  J. Alex Long
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random
from string import ascii_uppercase
import sys  # for .sgf support

BLACK = "X"
WHITE = "O"
EMPTY = "."
OTHER_SIDE = {BLACK: WHITE,
              WHITE: BLACK}
PASS = (-1, -1)


class Board:
    def __init__(self, size: int = 19):
        """Initializes a new Board object

        Args:
            size (int, optional): Indicates the size of the game board.
            Defaults to 19.
        """
        self.size = size
        self.turn = BLACK
        # create an empty board
        self.board = [
            [EMPTY for x in range(self.size)] for y in range(self.size)
        ]
        # reminder: 1, 1 in a game will be 0, 0 in self.board
        self.history = []

    def __str__(self):
        s = ""
        for y in range(self.size):
            for x in range(self.size):
                s += self.board[x][y]
                if len(s) % (19 + len("\n")) == 19:
                    s += "\n"
        return s

    def get_stone(self, coord):
        x, y = coord
        stone = self.board[x][y]
        return stone

    def place_stone(self, coord, color):
        x, y = coord
        self.board[x][y] = color

    def make_move(self, coord) -> bool:
        """Makes move in self.board, self.history and changes self.turn

        Args:
            coord (tuple): Move to be made in self.

        Returns:
            bool: True if successfully made move in board
                  False if unsuccessful
        """
        if self.move_is_legal(coord):
            self.place_stone(coord, self.turn)
            self.history.append(coord)
            self.turn = BLACK if self.turn == WHITE else WHITE
            return True
        else:
            return False

    def undo_last_move(self):
        last_move = self.history.pop()
        self.remove_stone(last_move)
        self.turn = OTHER_SIDE[self.turn]

    def move_is_legal(self, move) -> bool:
        stone = self.get_stone(move)
        if stone == EMPTY:
            return True
        elif stone == self.turn:
            return False
        return False

    def coord_string_to_coord_tuple(self, coord_string):
        # i.e. "C16" -> (3, 15) THIS METHOD DOESN'T WORK YET LOOK AT REAL BOARD
        x = ascii_uppercase.index(coord_string[0])
        y = int(coord_string[:1]) - 1
        return (x, y)

    def coord_tuple_to_coord_string(self, coord_tuple):
        # i.e. (3, 15) -> "C16"
        x, y = coord_tuple
        x = ascii_uppercase[x]
        y = y + 1
        return f"{x}{y}"

    def get_neighbors(self, coord: tuple) -> list:
        """returns list of stones in neighboring squares

        Args:
            coord (tuple): coordinate of point on the board in question

        Returns:
            list: [left, right, up, down]
        """
        x, y = coord
        left_stone = self.board[x-1][y] if x != 0 else None
        right_stone = self.board[x+1][y] if x != self.size else None
        up_stone = self.board[x][y-1] if y != 0 else None
        down_stone = self.board[x][y+1] if y != self.size else None

        neighbors = [left_stone, right_stone, up_stone, down_stone]
        return neighbors

    def remove_stone(self, coord: tuple):
        x, y = coord
        self.board[x][y] = EMPTY


class Engine:
    def __init__(self, board=None):
        # create a board for the engine if one isn't passed
        self.board = Board() if board is None else board

    def select_random_move(self) -> tuple:
        x = random.randint(0, self.board.size-1)
        y = random.randint(0, self.board.size-1)
        return (x, y)

    def make_engine_move(self):
        making_move = True
        i = 0
        while making_move:
            i += 1
            move = self.select_random_move()
            success = self.board.make_move(move)
            if success:
                making_move = False
        return success


class Group:
    def __init__(self, coord: tuple, board: object):
        self.color = board.get_stone(coord)
        # get first stone we've seen of the group
        self.stones = [coord]
        self.stones_seen = []
        self.liberties = []
        self.find_all_stones()

    def find_all_stones(self):
        """Uses recursion to find all ally stones
        This thing is a bit of a monster in terms of nesting...
        """
        # break the recursion if we've already gone over all coordinates
        if self.stones == self.stones_seen:
            return

        for stone in self.stones:
            # skip the stone if we've seen it before
            if stone in self.stones_seen:
                continue
            else:
                # note that we've looked at this stone now
                self.stones_seen.append(stone)
                neighbors = self.board.get_neighbors(stone)
                # look at the immediate neighboring points on the board
                for direction in neighbors:
                    x, y = direction
                    neighbor = self.board[x][y]
                    if neighbor == self.color:
                        self.stones.append(neighbor)
                        self.find_all_stones()
                    elif neighbor == EMPTY and neighbor not in self.liberties:
                        self.liberties.append(neighbor)
