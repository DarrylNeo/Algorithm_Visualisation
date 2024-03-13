import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0


class MCTS:
    def __init__(self, root_state):
        self.root = Node(root_state)

    def select(self, node):
        while node.children:
            node = self._uct_select(node)
        return node

    def _uct_select(self, node):
        UCT_CONSTANT = 1.414
        best_child = None
        best_score = -float('inf')

        for child in node.children:
            if child.visits == 0:
                score = float('inf')  # Ensure unvisited nodes are explored
            else:
                exploit = child.value / child.visits
                explore = np.sqrt(
                    np.log(node.visits) / (child.visits + 1e-6))  # Add small value to avoid division by zero
                score = exploit + UCT_CONSTANT * explore
            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def expand(self, node):
        actions = self._get_legal_actions(node.state)
        for action in actions:
            new_state = self._apply_action(node.state, action)
            new_node = Node(new_state, parent=node)
            node.children.append(new_node)
        return node.children[np.random.randint(len(node.children))]

    def simulate(self, node):
        return np.random.rand()

    def backpropagate(self, node, value):
        while node is not None:
            node.visits += 1
            node.value += value
            node = node.parent

    def _get_legal_actions(self, state):
        return [action for action in
                range(state + 1, state + 4)]  # Example: legal actions are the next 3 consecutive integers

    def _apply_action(self, state, action):
        return action

    def visualize_tree(self, iterations=100):
        fig, ax = plt.subplots(figsize=(10, 8))
        colormap = plt.cm.get_cmap('tab10')

        for i in range(iterations):
            graph = self._build_graph(self.root)
            colors = [colormap(i / iterations) for _ in range(len(graph.nodes()))]
            pos = nx.spring_layout(graph, scale=1000)  # Adjust scale for better spacing

            # Draw nodes with annotations
            node_labels = {node: str(node) for node in graph.nodes()}
            nx.draw_networkx_nodes(graph, pos, node_size=300, node_color=colors, ax=ax)
            nx.draw_networkx_labels(graph, pos, labels=node_labels, font_size=8, ax=ax)

            # Draw edges with corresponding colors
            edges = graph.edges()
            colors = [colormap(i / iterations) for _ in range(len(edges))]
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color=colors, ax=ax, width=1.0)

        ax.set_title('MCTS Tree Visualization')

        # Custom color bar legend
        for i in range(iterations):
            plt.scatter([], [], c=[colormap(i / iterations)], label=f"Iteration {i + 1}")

        plt.legend(scatterpoints=1, frameon=False, labelspacing=1, loc='upper left')
        plt.show()

    def _build_graph(self, node):
        graph = nx.DiGraph()
        queue = [node]
        while queue:
            current_node = queue.pop(0)
            for child in current_node.children:
                graph.add_edge(current_node.state, child.state)
                queue.append(child)
        return graph


# Example usage:
initial_state = 1  # Define your initial state, e.g., 1
mcts = MCTS(initial_state)
iterations = 2
for _ in range(iterations):  # Perform 5 iterations for simplicity
    node = mcts.select(mcts.root)
    if not node.children:
        node = mcts.expand(node)
    value = mcts.simulate(node)
    mcts.backpropagate(node, value)
mcts.visualize_tree(iterations)