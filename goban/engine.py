from game import Board
from random import randint


class Engine:
    def __init__(self, board = None):
        # create a Board for the engine if one isn't passed
        self.Board = Board() if Board is None else board

    def select_random_move(self) -> tuple:
        x = randint(0, self.board.size-1)
        y = randint(0, self.board.size-1)
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

'''
████████╗███████╗███████╗████████╗    ███████╗ ██████╗ ███╗   ██╗███████╗
╚══██╔══╝██╔════╝██╔════╝╚══██╔══╝    ╚══███╔╝██╔═══██╗████╗  ██║██╔════╝
   ██║   █████╗  ███████╗   ██║         ███╔╝ ██║   ██║██╔██╗ ██║█████╗
   ██║   ██╔══╝  ╚════██║   ██║        ███╔╝  ██║   ██║██║╚██╗██║██╔══╝
   ██║   ███████╗███████║   ██║       ███████╗╚██████╔╝██║ ╚████║███████╗
   ╚═╝   ╚══════╝╚══════╝   ╚═╝       ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
'''
