import numpy as np

class TicTacToe:

    def __init__(self, size=3):
        self.size = size
        self.board = np.zeros((size, size))
        self.player = 1

    def do_action(self, x,y, print_board=False):
        if self.is_terminal():
            print("Game is over. The last player to do action has won.")
            return
        if x < self.size and y < self.size:
            if self.board[x][y] == 0:
                self.board[x][y] = self.player
                self.player = -self.player
            else: 
                print("The square is already taken.")
        else: 
            print("Invalid square coordinates.")
        if print_board:
            print("Move: ", x,y)
            self.print_board()
        

    def print_board(self):

        for x in range(self.size + 2):
            print("#", end=" ")
        print()

        for x in range(self.size):
            print("#", end=" ")
            for y in range(self.size):
                sign = "-"
                if self.board[x][y] == 1:
                    sign = "X"
                elif self.board[x][y] == -1:
                    sign = "O"
                print(sign, end=" ")
            print("#")

        for x in range(self.size + 2):
            print("#", end=" ")
        print()

    def is_terminal(self):
        for i in range(self.size):
            start = self.board[i,0]
            if start != 0:
                for j in range(1,self.size):
                    if self.board[i,j] != start:
                        break
                    if j == self.size - 1:
                        return True
                    
        for i in range(self.size):
            start = self.board[0,i]
            if start != 0:
                for j in range(1,self.size):
                    if self.board[j,i] != start:
                        break
                    if j == self.size - 1:
                        return True

        start = self.board[0][0]   
        if start != 0:      
            for i in range(1,self.size):
                if self.board[i][i] != start:
                    break
                if i == self.size - 1:
                    return True
        
        start = self.board[0][self.size - 1]   
        if start != 0:      
            for i in range(1,self.size):
                if self.board[i][-i-1] != start:
                    break
                if i == self.size - 1:
                    return True
            
        return False

game = TicTacToe(4)
game.do_action(0,1)
game.do_action(0,2)
game.do_action(0,0)
game.do_action(0,3)
game.do_action(1,3)
