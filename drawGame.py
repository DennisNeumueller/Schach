import pygame

from pieces.Bishop import Bishop
from pieces.King import King
from pieces.Knight import Knight
from pieces.Pawn import Pawn
from pieces.Queen import Queen
from pieces.Rook import Rook

pygame.mixer.init()

move_sound = pygame.mixer.Sound("sounds/move_sound.mp3")
beat_sound = pygame.mixer.Sound("sounds/capture_sound.mp3")
check_sound = pygame.mixer.Sound("sounds/check_sound.mp3")
promote_sound = pygame.mixer.Sound("sounds/promote_sound.mp3")
funny_sound = pygame.mixer.Sound("sounds/metal_pipe.mp3")


class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.knight = Knight(self)
        self.rook = Rook(self)
        self.bishop = Bishop(self)
        self.queen = Queen(self)
        self.king = King(self)
        self.pawn = Pawn(self)
        self.all_moves = {"p": self.pawn.get_legal_moves, "R": self.rook.get_legal_moves,
                          "N": self.knight.get_legal_moves, "B": self.bishop.get_legal_moves,
                          "Q": self.queen.get_legal_moves, "K": self.king.get_legal_moves}
        self.white_to_move = True
        self.beaten_pieces = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.in_check = False
        self.move_log = []
        self.pins = []
        self.checks = []

    def play_move_sound(self):
        move_sound.play()

    def play_beat_sound(self):
        beat_sound.play()

    def play_check_sound(self):
        check_sound.play()

    def play_promote_sound(self):
        promote_sound.play()

    def play_sound(self):
        funny_sound.play()

    def make_move(self, move):

        self.board[move.start_row][move.start_col] = "--"
        if self.board[move.end_row][move.end_col] != "--":
            self.play_beat_sound()
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if self.board[move.start_row][move.start_col] == "--":
            self.play_move_sound()

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        if self.is_in_check():
            self.play_check_sound()

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
            self.play_promote_sound()

    def get_legal_moves(self):

        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins()

        if self.white_to_move:
            king_row = self.white_king_location[0]
            king_col = self.white_king_location[1]
        else:
            king_row = self.black_king_location[0]
            king_col = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:
                moves = self.get_all_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                piece_checking = self.board[check_row][check_col]
                valid_squares = []
                if piece_checking[1] == "N":
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].piece_moved[1] != "K":
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else:
                self.king.get_legal_moves(king_row, king_col, moves)
        else:
            moves = self.get_all_moves()

        if len(moves) == 0:
            if self.is_in_check():
                self.checkmate = True
        else:
            self.checkmate = False

        return moves

    def is_in_check(self):
        if self.white_to_move:
            return self.piece_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.piece_under_attack(self.black_king_location[0], self.black_king_location[1])

    def get_beaten_pieces(self):
        return self.beaten_pieces

    def piece_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move
        opponents_moves = self.get_all_moves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:
                return True
        return False

    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]
                    self.all_moves[piece](row, col, moves)
        return moves

    def check_for_pins(self):
        pins = []
        checks = []
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_row = self.white_king_location[0]
            start_col = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_row = self.black_king_location[0]
            start_col = self.black_king_location[1]

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        if ((0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or
                                (i == 1 and enemy_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or
                                (enemy_color == "b" and 4 <= j <= 5))) or (enemy_type == "Q") or
                                (i == 1 and enemy_type == "K")):
                            if possible_pin == ():
                                in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break
                            else:
                                pins.append(possible_pin)
                                break
                        else:
                            break
                else:
                    break  # off board
        return in_check, pins, checks

