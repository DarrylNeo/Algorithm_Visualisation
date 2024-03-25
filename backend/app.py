from flask import Flask, jsonify
from flask_cors import CORS

from monte_carlo_tree_search import MCTS
from tictactoe import TicTacToeBoard

def play_game():
    tree = MCTS()
    board = new_tic_tac_toe_board()
    
    row = 1
    col = 1
    index = 3 * (row - 1) + (col - 1)
    if board.tup[index] is not None:
        raise RuntimeError("Invalid move")
    board = board.make_move(index)
    # You can train as you go, or only at the beginning.
    # Here, we train as we go, doing fifty rollouts each turn.
    for _ in range(3):
        tree.do_rollout(board)
    global tictactoeData
    tictactoeData = tree.export_to_format(tree, next(iter(tree.children.keys())))

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

