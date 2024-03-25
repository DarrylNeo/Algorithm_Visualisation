import pygame as pg
import sys
import time
from pygame.locals import *

# GUI

XO = 'x'

winner = None

draw = None

width = 400

height = 400

white = (255, 255, 255)

line_color = (0, 0, 0)

board = [[None] * 3, [None] * 3, [None] * 3]

pg.init()

fps = 30

CLOCK = pg.time.Clock()

screen = pg.display.set_mode(
    (width, height + 100), 0, 32
)

pg.display.set_caption("Tic Tac Toe Test")

initiating_window = pg.image.load("tiktaktoecover.png")
x_img = pg.image.load("x.png")
y_img = pg.image.load("o.png")

initiating_window = pg.transform.scale(initiating_window, (width, height + 100))
x_img = pg.transform.scale(x_img, (80, 80))
y_img = pg.transform.scale(y_img, (80, 80))


def game_initialisation():
    screen.blit(initiating_window, (0, 0))

    pg.display.update()
    time.sleep(3)
    screen.fill(white)

    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 7)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 7)

    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 7)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 7)

    draw_screen()


def draw_screen():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " has won !"
    if draw and winner is None:
        message = "Draw!"

    font = pg.font.Font(None, 30)

    text = font.render(message, 1, (255, 255, 255))

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    screen.blit(text, text_rect)
    pg.display.update()


# algorithm to check for winner

def checking_win():
    global board, winner, draw

    # checking for winning rows
    for row in range(0, 3):
        if ((board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None)):
            winner = board[row][0]
            pg.draw.line(screen, (250, 0, 0),
                         (0, (row + 1) * height / 3 - height / 6),
                         (width, (row + 1) * height / 3 - height / 6),
                         4)
            break

    # checking for winning columns
    for col in range(0, 3):
        if ((board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None)):
            winner = board[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * width / 3 - width / 6, 0),
                         ((col + 1) * width / 3 - width / 6, height), 4)
            break

    # check for diagonal winners
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        # game won diagonally left to right
        winner = board[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        # game won diagonally right to left
        winner = board[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50), (50, 350), 4)

    if (all([all(row) for row in board]) and winner is None):
        draw = True
        draw_screen()


def tik_tak_toe_board(row, col):
    global board, XO

    if row == 1:
        posx = 30

    if row == 2:
        posx = width / 3 + 30

    if row == 3:
        posx = width / 3 * 2 + 30

    if col == 1:
        posy = 30

    if col == 2:
        posy = height / 3 + 30

    if col == 3:
        posy = height / 3 * 2 + 30

    board[row - 1][col - 1] = XO

    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = 'o'

    else:
        screen.blit(y_img, (posy, posx))
        XO = 'x'
    pg.display.update()


def user_actions():
    x, y = pg.mouse.get_pos()

    if x < (width / 3):
        col = 1
    elif x < (width / 3 * 2):
        col = 2
    elif x < width:
        col = 3
    else:
        col = None

    if y < (height / 3):
        row = 1
    elif y < (height / 3 * 2):
        row = 2
    elif y < height:
        row = 3
    else:
        row = None

    if row and col and (board[row - 1][col - 1] is None):
        global XO
        tik_tak_toe_board(row, col)
        checking_win()


def game_reset():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_initialisation()
    winner = None
    board = [[None] * 3, [None] * 3, [None] * 3]


game_initialisation()

while True:
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            user_actions()
            if winner or draw:
                game_reset()
    pg.display.update()
    CLOCK.tick(fps)