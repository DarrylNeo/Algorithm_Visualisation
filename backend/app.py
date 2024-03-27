from flask import Flask, jsonify
from flask_cors import CORS

from monte_carlo_tree_search import MCTS
from tictactoe import TicTacToe, TicTacToeBoard

app = Flask(__name__)
CORS(app)

# Runs MCTS tree on set domain
def run():
    tree = MCTS()
    domain = TicTacToe()
    domain.iterate(tree, 2)
    return domain.export_tree()

# Passes current MCTS tree
@app.route('/api/tree', methods=['GET'])
def get_tictactoe_data():
    return jsonify(run())

# First function that runs
if __name__ == '__main__':
    app.run(debug=True)

# Runs before the first api call, functions that 'print' will print to terminal here
with app.app_context():
    print("DEBUGGING TOOL")