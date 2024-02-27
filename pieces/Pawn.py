import Move

class Pawn():
    def __init__(self, game_state):
        self.game_state = game_state

    def get_legal_moves(self, row, col, moves):
        piece_pinned, pin_direction = self.check_pinned_piece(row, col)

        direction = 1 if self.game_state.white_to_move else -1
        start_row = 6 if self.game_state.white_to_move else 1

        self.add_single_square_move(row, col, direction, moves, piece_pinned)
        self.add_double_square_move(row, col, direction, start_row, moves, piece_pinned)

        self.add_capture_moves(row, col, direction, moves, piece_pinned)

    def check_pinned_piece(self, row, col):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.game_state.pins) - 1, -1, -1):
            if self.game_state.pins[i][0] == row and self.game_state.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.game_state.pins[i][2], self.game_state.pins[i][3])
                self.game_state.pins.remove(self.game_state.pins[i])
                break
        return piece_pinned, pin_direction

    def add_single_square_move(self, row, col, direction, moves, piece_pinned):
        if self.game_state.board[row - direction][col] == "--" and not piece_pinned:
            moves.append(Move.Move((row, col), (row - direction, col), self.game_state.board))

    def add_double_square_move(self, row, col, direction, start_row, moves, piece_pinned):
        if row == start_row and self.game_state.board[row - 2 * direction][col] == "--" and not piece_pinned:
            moves.append(Move.Move((row, col), (row - 2 * direction, col), self.game_state.board))

    def add_capture_moves(self, row, col, direction, moves, piece_pinned):
        for j in [-1, 1]:
            end_row = row - direction
            end_col = col + j
            if end_row <= 7 and end_col <= 7:
                end_piece = self.game_state.board[end_row][end_col]
                if end_piece[0] == ("b" if self.game_state.white_to_move else "w") and not piece_pinned:
                    moves.append(Move.Move((row, col), (end_row, end_col), self.game_state.board))
