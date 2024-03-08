import pygame

from Move import Move
from castleRights import CastleRights
from sound import Sound
from pieces.Bishop import Bishop
from pieces.King import King
from pieces.Knight import Knight
from pieces.Pawn import Pawn
from pieces.Queen import Queen
from pieces.Rook import Rook


class GameState:
    def __init__(self):
        #Chess board setup
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        #Instances of the chess pieces
        self.knight = Knight(self)
        self.rook = Rook(self)
        self.bishop = Bishop(self)
        self.queen = Queen(self)
        self.king = King(self)
        self.pawn = Pawn(self)
        self.all_moves = {"p": self.pawn.get_legal_moves, "R": self.rook.get_legal_moves,
                          "N": self.knight.get_legal_moves, "B": self.bishop.get_legal_moves,
                          "Q": self.queen.get_legal_moves, "K": self.king.get_legal_moves}
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.sound = Sound(self)

        #Game state variables
        self.white_to_move = True
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.move_log = []
        self.pins = []
        self.checks = []

    # Making a move on the chess board
    def make_move(self, move):

        self.board[move.start_row][move.start_col] = "--"

        if self.board[move.end_row][move.end_col] != "--":
            self.sound.play_beat_sound()

        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if self.board[move.start_row][move.start_col] == "--":
            self.sound.play_move_sound()

        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_col)

        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_col)

        if self.is_in_check():
            self.sound.play_check_sound()

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + "Q"
            self.sound.play_promote_sound()

        # castle move
        if move.can_castle:
            if move.end_col - move.start_col == 2:  # king-side castle move
                if move.end_col + 1 < len(self.board[0]):  # check if the index is within the valid range
                    self.board[move.end_row][move.end_col - 1] = self.board[move.end_row][move.end_col + 1]  # moves the rook to its new square
                    self.board[move.end_row][move.end_col + 1] = '--'  # erase old rook
                    self.sound.play_castle_sound()
            elif move.end_col - move.start_col == -2:  # queen-side castle move
                if move.end_col - 2 >= 0:  # check if the index is within the valid range
                    self.board[move.end_row][move.end_col + 1] = self.board[move.end_row][move.end_col - 2]  # moves the rook to its new square
                    self.board[move.end_row][move.end_col - 2] = '--'  # erase old rook
                    self.sound.play_castle_sound()

        self.update_castle_rights(move)

    def update_castle_rights(self, move):
        if move.piece_captured == "wR":
            if move.end_col == 0:  # left rook
                self.current_castling_rights.white_queen_side = False
            elif move.end_col == 7:  # right rook
                self.current_castling_rights.white_king_side = False

        elif move.piece_captured == "bR":
            if move.end_col == 0:  # left rook
                self.current_castling_rights.black_queen_side = False
            elif move.end_col == 7:  # right rook
                self.current_castling_rights.black_king_side = False

        if move.piece_moved == 'wK':
            self.current_castling_rights.white_queen_side = False
            self.current_castling_rights.white_king_side = False

        elif move.piece_moved == 'bK':
            self.current_castling_rights.black_queen_side = False
            self.current_castling_rights.black_king_side = False

        elif move.piece_moved == 'wR':
            if move.start_row == 7:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.white_queen_side = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.black_king_side = False

        elif move.piece_moved == 'bR':
            if move.start_row == 0:
                if move.start_col == 0:  # left rook
                    self.current_castling_rights.black_queen_side = False
                elif move.start_col == 7:  # right rook
                    self.current_castling_rights.black_king_side = False

    # Checking for the color of the opponent
    def check_enemy_color(self):
        enemy_color = "b" if self.white_to_move else "w"
        return enemy_color

    # Getting all legal moves
    def get_legal_moves(self):
        temp_castle_rights = CastleRights(self.current_castling_rights.white_king_side,
                                          self.current_castling_rights.black_king_side,
                                          self.current_castling_rights.white_queen_side,
                                          self.current_castling_rights.black_queen_side)

        moves = []
        self.in_check, self.pins, self.checks = self.check_for_pins()
        king_row, king_col = (self.white_king_location if self.white_to_move else self.black_king_location)

        if self.in_check:
            if len(self.checks) == 1:
                moves = self.filter_moves_by_check(king_row, king_col)

            else:
                self.king.get_legal_moves(king_row, king_col, moves)

        else:
            moves = self.get_all_moves()
            if self.white_to_move:
                self.get_castle_moves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.get_castle_moves(self.black_king_location[0], self.black_king_location[1], moves)

        self.check_checkmate(moves)
        self.current_castling_rights = temp_castle_rights
        return moves

    # Filtering the moves if the king is in check, so that the pieces cannot move if they are blocking the check on the king
    def filter_moves_by_check(self, king_row, king_col):
        moves = self.get_all_moves()
        check = self.checks[0]
        check_row, check_col, piece_checking = check[0], check[1], self.board[check[0]][check[1]]
        valid_moves = []

        if piece_checking[1] == "N":
            valid_moves = [(check_row, check_col)]
        else:
            for i in range(1, 8):
                valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                valid_moves.append(valid_square)

                if valid_square[0] == check_row and valid_square[1] == check_col:
                    break

        for i in range(len(moves) - 1, -1, -1):
            if moves[i].piece_moved[1] != "K":
                if not (moves[i].end_row, moves[i].end_col) in valid_moves:
                    moves.remove(moves[i])

        moves = [move for move in moves if move.piece_moved[1] == "K" or (move.end_row, move.end_col) in valid_moves]
        return moves

    # Checkmate method
    def check_checkmate(self, moves):
        if len(moves) == 0:
            if self.is_in_check():
                self.checkmate = True
                self.sound.play_game_end_sound()
            else:
                self.stalemate = True
                self.sound.play_game_end_sound()
        else:
            self.checkmate = False
            self.stalemate = False

    # Checking if the king is in check
    def is_in_check(self):
        if self.white_to_move:
            return self.piece_under_attack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.piece_under_attack(self.black_king_location[0], self.black_king_location[1])

    # Checking if the piece is under attack, so it can't move its position from the king
    def piece_under_attack(self, row, col):
        self.white_to_move = not self.white_to_move
        opponents_moves = self.get_all_moves()
        self.white_to_move = not self.white_to_move

        for move in opponents_moves:
            if move.end_row == row and move.end_col == col:
                return True

        return False

    # Getting all Movements of the pieces
    def get_all_moves(self):
        moves = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                turn = self.board[row][col][0]  # Determine the color and type of the piece at the current position

                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[row][col][1]  # Type of the piece like Queen, King, Knight, pawn, Bishop
                    self.all_moves[piece](row, col, moves)

        return moves

    # Check if the piece is pinned, every piece, but not the king of course
    def check_for_pins(self):
        pins = []
        checks = []
        in_check = False

        ally_color, enemy_color, start_row, start_col = self.get_colors_and_pos()

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

        for j in range(len(directions)):    # Iterate over each direction
            direction = directions[j]
            possible_pin = ()

            for i in range(1, 8):  # Iterate over the board
                end_row = start_row + direction[0] * i
                end_col = start_col + direction[1] * i

                if 0 <= end_row <= 7 and 0 <= end_col <= 7:  # Within the board
                    end_piece = self.board[end_row][end_col]

                    if end_piece[0] == ally_color and end_piece[1] != "K":  # Current Player and not King
                        if possible_pin == ():  # No possible pin yet
                            possible_pin = (end_row, end_col, direction[0], direction[1])
                        else:
                            break  # Possible pin exists, but another piece of the same color is found

                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]

                        if self.is_check_or_pin(i, j, enemy_type):  # Check if opponent can give check or pin
                            if possible_pin == ():  # No possible pin yet
                                in_check = True  # If piece can give check, in_check = True
                                checks.append((end_row, end_col, direction[0], direction[1]))
                                break

                            else:
                                pins.append(possible_pin)  # If piece can give pin, append in pins
                                break
                        else:
                            break  # opponent's piece cannot give a check or pin, break loop
                else:
                    break  # end position off board, break loop

        # check for knight checks, because it doesn't recognize the knight moves
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_row = start_row + move[0]
            end_col = start_col + move[1]
            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_row, end_col, move[0], move[1]))

        return in_check, pins, checks

    # Getting colors and king pos
    def get_colors_and_pos(self):
        if self.white_to_move:
            return "w", "b", self.white_king_location[0], self.white_king_location[1]
        else:
            return "b", "w", self.black_king_location[0], self.black_king_location[1]

    # Checks for a pin or a check from the enemy
    def is_check_or_pin(self, i, j, enemy_type):
        enemy_color = self.check_enemy_color()
        return ((0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or
                (i == 1 and enemy_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or
                (enemy_color == "b" and 4 <= j <= 5))) or (enemy_type == "Q") or (i == 1 and enemy_type == "K"))

    def get_castle_moves(self, row, col, moves):
        if self.piece_under_attack(row, col):
            return  # can't castle while in check

        if ((self.white_to_move and self.current_castling_rights.white_king_side) or
                (not self.white_to_move and self.current_castling_rights.black_king_side)):
            self.get_king_side_castle(row, col, moves)

        if ((self.white_to_move and self.current_castling_rights.white_queen_side) or
                (not self.white_to_move and self.current_castling_rights.black_queen_side)):
            self.get_queen_side_castle(row, col, moves)

    def get_king_side_castle(self, row, col, moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.piece_under_attack(row, col + 1) and not self.piece_under_attack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, can_castle=True))

    def get_queen_side_castle(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.piece_under_attack(row, col - 1) and not self.piece_under_attack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, can_castle=True))

