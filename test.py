import WildeStone as wildeStone

def testGame():
    """tests the Game class by making 10 moves."""
    testGame = wildeStone.Game()
    for i in range(10):
        move = testGame.engine.selectMove()
        testGame.board.makeMove(move)
        print(testGame.engine.board, '\n'*2)
        
testGame()