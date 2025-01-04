from goban import Board
from random import randint


class Engine:
    def __init__(self, Board=None):
        # create a Board for the engine if one isn't passed
        self.Board = Board() if Board is None else Board

    def select_random_move(self) -> tuple:
        x = randint(0, self.Board.size-1)
        y = randint(0, self.Board.size-1)
        return (x, y)

    def make_engine_move(self):
        making_move = True
        i = 0
        while making_move:
            i += 1
            move = self.select_random_move()
            success = self.Board.make_move(move)
            if success:
                making_move = False
        return success

'''
████████╗███████╗███████╗████████╗    ███████╗ ██████╗ ███╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝    ╚══███╔╝██╔═══██╗████╗  ██║██╔════╝
   ██║   █████╗  ███████╗   ██║         ███╔╝ ██║   ██║██╔██╗ ██║█████╗
   ██║   ██╔══╝  ╚════██║   ██║        ███╔╝  ██║   ██║██║╚██╗██║██╔══╝
   ██║   ███████╗███████║   ██║       ███████╗╚██████╔╝██║ ╚████║███████╗
   ╚═╝   ╚══════╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
'''

def ten_move_game():
    """plays a game by making 10 moves."""
    engine = Engine()
    for i in range(10):
        engine.make_engine_move()
        print(f"Turn {i+1}:\n=======\n{engine.Board}\n\n")
    return True

def hundred_move_game():
    """plays a game by making 10 moves."""
    engine = Engine()
    for i in range(100):
        engine.make_engine_move()
        print(f"Turn {i+1}:\n=======\n{engine.Board}\n\n")
    return True


goban = hundred_move_game()
last_move = goban.history.pop()
"""first_group = Group(last_move, Board)

print(f"Here are all of the stones in the group at {last_move}:")
print(f"Stones: {first_group.stones}")
print(f"Liberties: {len(first_group.liberties)}")
"""
