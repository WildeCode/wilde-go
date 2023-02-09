from Board import *

def testRun():
    moveList = [(0, 0), ()]
    gameBoard = Board()
    gameBoard.makeMove((18, 0))
    gameBoard.makeMove((1, 1))
    gameBoard.makeMove((1, 2))
    gameBoard.makeMove((1, 1))
    print(gameBoard)

if __name__ == "__main__":
    testRun()
