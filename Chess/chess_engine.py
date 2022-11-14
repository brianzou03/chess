"""
This class stores all information about the current state of a chess game.
Also responsible for determining valid moves at the current state.
Also keeps a log of moves.
"""


class GameState:
    def __init__(self):
        # board is 8x8 matrix, each element has 2 chars
        # first char represents color, second represents type
        # "--" represents an empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.white_to_move = True
        self.move_log = []

    # Takes Move as a param and executes (does not work for castling, pawn promotion, and en-passant)
    def make_move(self, move):
        self.board[move.start_row][move.start_col] = "--"  # make a piece blank after moving it
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)  # log the move for undo later/game history
        self.white_to_move = not self.white_to_move  # switch turns

    # Undo last move made
    def undoMove(self):
        if len(self.move_log) != 0:  # ensure there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved  # move the piece back
            self.board[move.end_row][move.end_col] = move.piece_captured  # return the captured piece back
            self.white_to_move = not self.white_to_move  # switch turns back

    # Checking all moves with checks
    def get_valid_moves(self):
        return self.get_all_possible_moves()  # temporarily not focusing on checks

    # Checking all moves without checks
    def get_all_possible_moves(self):
        moves = [Move((6,4), (4,4), self.board)]  # temp allow one possible move
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                if (color == 'w' and self.white_to_move) and (color == 'b' and not self.white_to_move):  # or?
                    piece = self.board[r][c][1]
                    if piece == 'P':
                        self.get_pawn_moves(r, c, moves)  # get possible moves for specific pawn and add to moves
                    elif piece == 'R':
                        self.get_rook_moves(r, c, moves)

        return moves


    # Get all possible pawn moves for specific pawn at row, col, and add the moves to the list
    def get_pawn_moves(self, r, c, moves):
        pass

    # Get all possible rook moves for specific pawn at row, col, and add the moves to the list
    def get_rook_moves(self, r, c, moves):
        pass


class Move:
    # map keys to values
    # key : value
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}  # reverses k,v in dictionary

    files_to_cols = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}

    cols_to_files = {v: k for k, v in files_to_cols.items()}

    def __init__(self, start_sq, end_sq, board):
        self.start_row = start_sq[0]
        self.start_col = start_sq[1]
        self.end_row = end_sq[0]
        self.end_col = end_sq[1]
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col  # generate a unique move id between 0 - 7777
        print(self.moveID)

    # Overriding equals method
    def __eq__(self, other):  # compare an object to another object
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def get_chess_notation(self):  # return rank-file notation (not fully proper chess notation)
        return self.get_rank_file(self.start_row, self.start_col) + self.get_rank_file(self.end_row, self.end_col)

    def get_rank_file(self, r, c):
        return self.cols_to_files[c] + self.rows_to_ranks[r]  # file then rank in chess notation










