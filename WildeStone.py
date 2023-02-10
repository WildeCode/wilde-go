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
import sys # for .sgf support

BLACK = "X"
WHITE = "O"
EMPTY = "-"
PASS = (-1, -1)

class Board:
    def __init__(self, size: int = 19) -> None:
        """Initializes a new Board object

        Args:
            size (int, optional): Indicates the size of the game board. Defaults to 19.
        """
        self.size = size
        self.turn = BLACK
        # create an empty board
        self.board = [
            ['-' for x in range(self.size)] for x in range(self.size)
        ]
        # reminder: 1, 1 in a game will be 0, 0 in self.board

    def __str__(self) -> str:
        s = ''
        for y in range(self.size):
            for x in range(self.size):
                s += self.board[x][y]
                if len(s) % (19 + len('\n')) == 19:
                    s += '\n'
        return s

    def makeMove(self, move) -> None:
        """Makes move in self.board and changes self.turn

        Args:
            move (tuple): Move to be made in self.
        """
        if self.moveIsLegal(move, self.turn):
            x, y = move
            self.board[x][y] = self.turn
            self.turn = BLACK if self.turn == WHITE else WHITE


    def moveIsLegal(self, move, color) -> bool:
        x, y = move
        if self.board[x][y] == EMPTY:
            return True
        elif self.board[x][y] == color:
            return False
        return False

    def coordToMove(self, coord: str) -> tuple:
        """Converts coordinates to engine move format.
        Currently, the schema for the formats is undecided.

        Args:
            coord (str)): alphanumerical form of coordinates (i.e. 'A1')

        Returns:
            tuple: engine move format of layman coordinates (i.e. (0, 0))
        """
        x = y = 0
        return (x, y)

    def moveToCoord(self, move: tuple) -> str:
        return ''
    

class Engine:
    def __init__(self, board: list = Board()) -> None:
        self.board = Board()
    
    def selectMove(self) -> tuple:
        x = random.randint(0, self.board.size-1)
        y = random.randint(0, self.board.size-1)
        return (x, y)
        
    def makeMove(self) -> None:
        move = self.selectMove()
        self.board.makeMove(move)
        

class CLI:
    def __init__(self):
        pass

        
class Game:
    def __init__(self, players: int = 0, size: int = 19) -> None:
        """Start a game of Go with the WildeStone engine

        Args:
            players (int): the number of human players
            players = 0 -> EvE
            players = 1 -> PvE
            players = 2 -> PVP
        """
        self.engine = Engine()
        self.board = self.engine.board
        