from flask import Flask, jsonify
from flask_cors import CORS


from collections import namedtuple
from random import choice
from monte_carlo_tree_search import MCTS, Node

_TTTB = namedtuple("TicTacToeBoard", "tup turn winner terminal")

id = 0
# Inheriting from a namedtuple is convenient because it makes the class
# immutable and predefines __init__, __repr__, __hash__, __eq__, and others
class TicTacToeBoard(_TTTB, Node):
    def __new__(cls, tup, turn, winner, terminal):
        global id
        self = super(TicTacToeBoard, cls).__new__(cls, tup, turn, winner, terminal)
        self.id = id
        print(self.id)
        id += 1
        return self

    def find_children(board):
        if board.terminal:  # If the game is finished then no moves can be made
            return set()
        # Otherwise, you can make a move in each of the empty spots
        return {
            board.make_move(i) for i, value in enumerate(board.tup) if value is None
        }

    def find_random_child(board):
        if board.terminal:
            return None  # If the game is finished then no moves can be made
        empty_spots = [i for i, value in enumerate(board.tup) if value is None]
        return board.make_move(choice(empty_spots))

    def reward(board):
        if not board.terminal:
            raise RuntimeError(f"reward called on nonterminal board {board}")
        if board.winner is board.turn:
            # It's your turn and you've already won. Should be impossible.
            raise RuntimeError(f"reward called on unreachable board {board}")
        if board.turn is (not board.winner):
            return 0  # Your opponent has just won. Bad.
        if board.winner is None:
            return 0.5  # Board is a tie
        # The winner is neither True, False, nor None
        raise RuntimeError(f"board has unknown winner type {board.winner}")

    def is_terminal(board):
        return board.terminal

    def make_move(board, index):
        tup = board.tup[:index] + (board.turn,) + board.tup[index + 1 :]
        turn = not board.turn
        winner = _find_winner(tup)
        is_terminal = (winner is not None) or not any(v is None for v in tup)
        newBoard = TicTacToeBoard(tup, turn, winner, is_terminal)
        return newBoard

    def to_pretty_string(board):
        to_char = lambda v: ("X" if v is True else ("O" if v is False else " "))
        rows = [
            [to_char(board.tup[3 * row + col]) for col in range(3)] for row in range(3)
        ]
        return (
            "\n  1 2 3\n"
            + "\n".join(str(i + 1) + " " + " ".join(row) for i, row in enumerate(rows))
            + "\n"
        )

    def getID(self):
        return self.id
        
    def __str__(self):
        return self.id


def play_game():
    tree = MCTS()
    board = new_tic_tac_toe_board()
    print(board.to_pretty_string())
    
    row_col = input("enter row,col: ")
    row, col = map(int, row_col.split(","))
    index = 3 * (row - 1) + (col - 1)
    if board.tup[index] is not None:
        raise RuntimeError("Invalid move")
    board = board.make_move(index)
    print(board.to_pretty_string())
    """ if board.terminal:
        break """
    # You can train as you go, or only at the beginning.
    # Here, we train as we go, doing fifty rollouts each turn.
    for _ in range(3):
        tree.do_rollout(board)
    global tictactoeData
    tictactoeData = tree.export_to_format(tree, next(iter(tree.children.keys())))
    board = tree.choose(board)
    print(board.to_pretty_string())
    """ if board.terminal:
        break """


def _winning_combos():
    for start in range(0, 9, 3):  # three in a row
        yield (start, start + 1, start + 2)
    for start in range(3):  # three in a column
        yield (start, start + 3, start + 6)
    yield (0, 4, 8)  # down-right diagonal
    yield (2, 4, 6)  # down-left diagonal


def _find_winner(tup):
    "Returns None if no winner, True if X wins, False if O wins"
    for i1, i2, i3 in _winning_combos():
        v1, v2, v3 = tup[i1], tup[i2], tup[i3]
        if False is v1 is v2 is v3:
            return False
        if True is v1 is v2 is v3:
            return True
    return None


def new_tic_tac_toe_board():
    return TicTacToeBoard(tup=(None,) * 9, turn=True, winner=None, terminal=False)

app = Flask(__name__)
CORS(app)

# Sample data
data = {
    "message": "Flask Backend"
}

global tictactoeData

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

@app.route('/api/tictactoe', methods=['GET'])
def get_tictactoe_data():
    return jsonify(tictactoeData)

with app.app_context():
    play_game()

if __name__ == '__main__':
    app.run(debug=True)

