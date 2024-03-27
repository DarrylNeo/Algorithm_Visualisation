from flask import Flask, jsonify
from flask_cors import CORS

from monte_carlo_tree_search import MCTS
from tictactoe import TicTacToe, TicTacToeBoard, Node

app = Flask(__name__)
CORS(app)

global tree
tree = None

# Runs MCTS tree on set domain
def create():
    global tree

    domain = TicTacToe()
    root = domain.get_root()
    tree = MCTS(root)
    tree.iterate(1)
    return tree.export()

# Creates and responds with MCTS tree
@app.route('/api/tree', methods=['GET'])
def create_tree():
    return jsonify(create())

# Conducts iteration on and responds with current MCTS tree
@app.route('/api/tree/iterate', methods=['GET'])
def iterate_tree():
    if tree is not None:
        tree.iterate(1)
        return jsonify(tree.export())
    else:
        return 'Tree not created yet', 400

# First function that runs
if __name__ == '__main__':
    app.run(debug=True)

# Runs before the first api call, functions that 'print' will print to terminal here
with app.app_context():
    print("DEBUGGING TOOL")