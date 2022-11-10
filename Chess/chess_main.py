"""Main driver file.
Handles user input, displays current GameState object.
"""

import pygame as p
from Chess import chess_engine

WIDTH = HEIGHT = 512  # size of window
DIMENSION = 8  # dimensions of the chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations
IMAGES = {}

'''
Initialize a global dictionary of images. Called once in main.
'''


def load_images():
    pieces = ["wP", "wR", "wN", "wB", "wK", "wQ", "bP", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:  # load pieces and scale them to size, store in dictionary
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
The main driver for our code.
Handles user input and updates graphics
"""


def main():
    p.init()  # initialize PyGame
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))  # temporarily filling with white
    gs = chess_engine.GameState()  # create gs (gamestate) object
    # print(gs.board)
    load_images()  # load images
    running = True
    sq_selected = ()  # no square selected initially, keeps track of last click of user - tuple: (row, col)
    player_clicks = []  # keeps track of player clicks - two tuples: e.g. [(6,4), (4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:  # quits when we hit x
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):  # user clicked same square twice
                    sq_selected = ()
                    player_clicks = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                if len(player_clicks) == 2:  # after both clicks used
                    move = chess_engine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = ()  # reset clicks
                    player_clicks = []
        draw_game_state(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Used for all graphics in current game state
"""


def draw_game_state(screen, gs):
    draw_board(screen)  # draws squares on board
    # adding pin piece highlighting and move suggestions are done here
    draw_pieces(screen, gs.board)  # draws pieces on top of squares


"""
Draws squares on board.
Top left square is always light.
Light squares have even values, dark squares have odd values
"""
def draw_board(screen):
    # colors = [p.Color("white"), p.Color("gray")]  # for default board colors
    colors = [p.Color(252, 242, 230), p.Color(114, 150, 87)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draws pieces on board using current GameState.board
"""
def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]  # access pieces from board in chess_engine
            if piece != "--":  # non empty square
                screen.blit(IMAGES[piece],
                            p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  # fetch piece from dictionary


if __name__ == "__main__":
    main()
