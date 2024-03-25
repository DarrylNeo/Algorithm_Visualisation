import math
import random
class Node:
    def __init__(self, state, game):
        self.state = state
        self.visited = 0
        self.nodeValue = 0
        self.children = []
        self.lose = 0
        self.win = 0
        self.game = game

    def selectedNode (node):
        bestChildNode = None
        bestUctValue = float('-inf')


        for childNode in node.children:

            #exploration value is the sqrt of the log of total visits to parent node divided by
            #the visits to the children node.

            explorationValue = math.sqrt(2 * math.log(node.visited) / childNode.visited)

            #exploitation value can be calculated by the value of the child node vs the number of visits
            #to the child node.

            exploitationValue = childNode.value / childNode.visited

            uctValue = explorationValue + exploitationValue

            if uctValue > bestUctValue:
                bestUctValue = uctValue
                bestChildNode = childNode

            return bestChildNode

    def expandTree(node):

        possibleMoves = node.game.get_possible_moves()
        for move in possibleMoves:
            newGameState = node.game.apply_move(move)
            newNode = Node(newGameState, node.game)
            node.children.append(newNode)

    def simulateGameState(node):
        currentState = node.state.clone()
        while not currentState.checking_win():
            possibleMoves = currentState.get_possible_moves()
            randomMove = random.choice(possibleMoves)
            currentState.apply_move(randomMove)
        return currentState.evaluate()

