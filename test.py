import WildeStone as ws


def ten_move_game():
    """plays a game by making 10 moves."""
    engine = ws.Engine()
    for i in range(10):
        engine.make_engine_move()
        print(f"Turn {i+1}:\n=======\n{engine.board}\n\n")
    return True


def hundred_move_game():
    """plays a game by making 10 moves."""
    engine = ws.Engine()
    for i in range(100):
        engine.make_engine_move()
        print(f"Turn {i+1}:\n=======\n{engine.board}\n\n")
    return True


board = hundred_move_game()
last_move = board.history.pop()
"""first_group = Group(last_move, board)

print(f"Here are all of the stones in the group at {last_move}:")
print(f"Stones: {first_group.stones}")
print(f"Liberties: {len(first_group.liberties)}")
"""
