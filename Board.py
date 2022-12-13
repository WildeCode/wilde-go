# Wilde-Stone Board class
# v0.0.1
# By J. Alexander Long
# 12-12-2022

BLACK = "X"
WHITE = "O"
EMPTY = "-"
PASS = (-1, -1)

class Board:
    def __init__(self, size=19):
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

    def __str__(self):
        s = ''
        for y in range(self.size):
            for x in range(self.size):
                s += self.board[x][y]
                if len(s) % (19 + len('\n')) == 19:
                    s += '\n'
        return s

    def makeMove(self, move):
        """Makes move in self.board and changes self.turn

        Args:
            move (tuple): Move to be made in self.
        """
        if self.moveIsLegal(move, self.turn):
            x, y = move
            self.board[x][y] = self.turn
            self.turn = BLACK if self.turn == WHITE else WHITE


    def moveIsLegal(self, move, color):
        x, y = move
        if self.board[x][y] == EMPTY:
            return True
        elif self.board[x][y] == color:
            return False
        return False

    def coordToMove(self, coord):
        """Converts coordinates to engine move format.
        Currently, the schema for the formats is undecided.

        Args:
            coord (str)): layman form of coordinates (i.e. 'A1')

        Returns:
            tuple: engine move format of layman coordinates (i.e. (0, 0))
        """
        x = y = 0
        return (x, y)

    def moveToCoord(self, move):
        return False

def testRun():
    moveList = [(0, 0), ()]
    gameBoard = Board()
    gameBoard.makeMove((18, 0))
    print(gameBoard)
    gameBoard.makeMove((1, 1))
    print(gameBoard)
    gameBoard.makeMove((1, 2))
    print(gameBoard)
    gameBoard.makeMove((1, 1))
    print(gameBoard)

if __name__ == "__main__":
    testRun()
