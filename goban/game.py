from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple



class Stone(IntEnum):
    BLACK = 0
    WHITE = 1

class Point(Tuple[int, int]):
    """
    Represents a point on the Go board.
    Inherits from tuple for immutability and efficiency.
    """
    def __new__(cls, row: int, col: int) -> 'Point':
        """
        Creates a new Point instance.

        Args:
            row: Row coordinate (1-indexed).
            col: Column coordinate (1-indexed).

        Returns:
            A new Point instance.
        """
        return super().__new__(cls, (row, col))

    @classmethod
    def from_str(cls, coord: str) -> 'Point':
        """
        Creates a Point instance from a string representation.

        Args:
            coord: String representation of the point in the format "A1", "B3", etc.
                   (Column letter followed by row number).

        Returns:
            A new Point instance.

        Raises:
            ValueError: If the input string is invalid.
        """
        # The letter 'I' isn't included to avoid confusion with 'J'
        valid_col_letters = "ABCDEFGHJKLMNOPQRST"
        if not coord or len(coord) not in [2, 3]:
            raise ValueError(f"Invalid coordinate format: {coord}")

        col_letter = coord[0].upper()
        if col_letter not in valid_col_letters:
            raise ValueError(f"Invalid column letter: {col_letter}")
        col = ord(col_letter) - ord('A') + 1
        # adjust offset to account for missing 'I' in valid_col_letters
        if col_letter in valid_col_letters[8:]:
            col -= 1

        try:
            row = int(coord[1:])
        except ValueError:
            raise ValueError(f"Invalid row number: {coord[1:]}")

        return cls(row, col)

    def __str__(self) -> str:
        """
        Returns a string representation of the point.

        Returns:
            String representation of the point in the format "A1", "B3", etc.
        """
        col_letter = chr(ord('A') + self.col - 1)
        return f"{col_letter}{self.row}"

@dataclass
class Move:
    turn_number: int
    point: Point
    stone: Stone | None

class Group:
    def find_members(self):
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
            # note that we've looked at this stone now
            self.stones_seen.append(stone)
            neighbors = self.Board.get_neighbors(stone)
            # look at the immediate neighboring points on the Board
            for direction in neighbors:
                x, y = direction
                neighbor = self.Board[x][y]
                if neighbor == self.color:
                    self.stones.append(neighbor)
                    self.find_members()
                elif neighbor != None and neighbor not in self.liberties:
                    self.liberties.append(neighbor)


class Board:
    def __init__(self, size: int = 19):
        """Initializes a new Board object

        Args:
            size (int, optional): Indicates the size of the game Board.
            Defaults to 19.
        """
        self.size = size
        # create an empty Board
        self.state = (
            (None for _ in range(self.size)) for _ in range(self.size)
        )

    def __str__(self):
        s = ""
        for y in range(self.size):
            for x in range(self.size):
                s += self.state[x][y] if type(self.state[x][y]) == Stone else '.'
                if len(s) % (self.size + len("\n")) == self.size:
                    s += "\n"
        return s

    def __eq__(self, other):
        for x in range(len(self)):
            for y in range(len(self)):
                if self.state[x][y] != other.state[x][y]:
                    return False
        return True

    def __len__(self):
        return self.size

    def get_stone(self, point: Point):
        x, y = point
        stone = self.state[x][y]
        return stone

    def place_stone(self, coord, color):
        x, y = coord
        self.Board[x][y] = color

    def make_move(self, coord) -> bool:
        """Makes move in self.Board, self.history and changes self.turn

        Args:
            coord (tuple): Move to be made in self.

        Returns:
            bool: True if successfully made move in Board
                  False if unsuccessful
        """
        if self.move_is_legal(coord):
            self.place_stone(coord, self.turn)
            self.history.append(coord)
            self.turn = BLACK if self.turn == WHITE else WHITE
            return True
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
        # i.e. "C16" -> (3, 15) THIS METHOD DOESN'T WORK YET LOOK AT REAL Board
        x = LETTERS.index(coord_string[0])
        y = int(coord_string[:1]) - 1
        return (x, y)

    def coord_tuple_to_coord_string(self, coord_tuple):
        # i.e. (3, 15) -> "C16"
        x, y = coord_tuple
        x = LETTERS[x]
        y = y + 1
        return f"{x}{y}"

    def get_neighbors(self, coord: tuple) -> list:
        """returns list of stones in neighboring squares

        Args:
            coord (tuple): coordinate of point on the Board in question

        Returns:
            list: [left, right, up, down]
        """
        x, y = coord
        left_stone = self.Board[x-1][y] if x != 0 else None
        right_stone = self.Board[x+1][y] if x != self.size else None
        up_stone = self.Board[x][y-1] if y != 0 else None
        down_stone = self.Board[x][y+1] if y != self.size else None

        neighbors = [left_stone, right_stone, up_stone, down_stone]
        return neighbors

    def remove_stone(self, coord: tuple):
        x, y = coord
        self.Board[x][y] = EMPTY


class Game:
    ok = True