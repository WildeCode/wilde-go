from dataclasses import dataclass
from enum import (
    Enum,
    IntEnum,
)
from typing import (
    Optional,
    Tuple,
    Union,
)


class Stone(IntEnum):
    BLACK = 0
    WHITE = 1

    def opposite_color(self) -> 'Stone':
        if self == Stone.BLACK:
            return Stone.WHITE
        elif self == Stone.WHITE:
            return Stone.BLACK

class Point(Tuple[int, int]):
    """
    Represents a point on the Go board.
    Inherits from typing.Tuple for immutability and efficiency.
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
        # The letter 'I' is commonly excluded to avoid confusion with 'J'
        valid_col_letters = "ABCDEFGHJKLMNOPQRST"
        if not coord or len(coord) not in [2, 3]:
            raise ValueError(f"Invalid coordinate format: {coord}")

        col_letter = coord[0].upper()
        if col_letter not in valid_col_letters:
            raise ValueError(f"Invalid column letter: {col_letter}")
        col = ord(col_letter) - ord('A') + 1
        # adjust offset to account for missing 'I' in valid_col_letters
        if col_letter in valid_col_letters[7:]:
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
        # adjusts offset to account for missing 'I' in valid_col_letters
        col_letter = chr(ord('A') + self.col - 1) if self.col <= 8 else chr(ord('A') + self.col)
        return f"{col_letter}{self.row}"

@dataclass
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
            (None for col in range(self.size)) for row in range(self.size)
        )

    def __getitem__(self, point: Point) -> Optional[Stone]:
        x, y = point
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.state[x][y]
        else:
            raise IndexError("Index out of bounds")

    def __setitem__(self, point: Point, stone: Stone):
        x, y = point
        if 0 <= x < self.size and 0 <= y < self.size:
            self.state[x][y] = stone
        else:
            raise IndexError("Index out of bounds")

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
                if self[x][y] != other[x][y]:
                    return False
        return True

    def __len__(self):
        return self.size

    def __iter__(self):
        """
        Returns an iterator over the board's points.
        """
        class BoardIterator:
            def __init__(self, board):
                self.board = board
                self.x = 0
                self.y = 0

            def __next__(self):
                if self.x >= self.board.size:
                    raise StopIteration
                point = (self.x, self.y)
                self.y += 1
                if self.y >= self.board.size:
                    self.y = 0
                    self.x += 1
                return point

        return BoardIterator(self)


@dataclass
class Move:
    turn_number: int
    point: Point
    stone: Stone

    def is_legal(self, board: Board) -> bool:
        return True


class PlayerType(IntEnum):
    PLAYER = 0
    CPU    = 1

@dataclass
class Player:
    name: str
    type: PlayerType
    stone: Stone

@ dataclass
class Game:
    player1: Player
    player2: Player
    turn: Stone = Stone.BLACK
    komi: float = 6.5
    board: Board = Board()
    history: list = []

    def make_move(self, move: Move):
        """Makes move in self.Board, self.history and changes self.turn

        Args:
            point (Point): Move to be made in self.
        """
        if self.move_is_legal(move, self.board):
            self.place_stone(move.stone)
            self.history.append(move)
            self.turn = self.turn.opposite_color()
        else:
            raise ValueError(f"The move {}")

    def undo_last_move(self):
        last_move = self.history.pop()
        self.remove_stone(last_move)
        self.turn = self.turn.opposite_color()

    def move_is_legal(self, move) -> bool:
        return True

    def get_neighbors(self, point: Point) -> list[Stone]:
        """returns list of stones in neighboring squares

        Args:
            point (Point): coordinate of point on the Board in question

        Returns:
            list: [left, right, up, down]
        """
        x, y = point
        left_stone = self.Board[x-1][y] if x != 0 else None
        right_stone = self.Board[x+1][y] if x != self.size else None
        up_stone = self.Board[x][y-1] if y != 0 else None
        down_stone = self.Board[x][y+1] if y != self.size else None

        neighbors = [left_stone, right_stone, up_stone, down_stone]
        return neighbors
