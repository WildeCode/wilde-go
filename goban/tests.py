from goban.engine import Engine


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

if __name__ == '__main__':
    print(ten_move_game())
    print(hundred_move_game())