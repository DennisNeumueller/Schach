from Move import Move

class King():
    def __init__(self, game_state):
        self.game_state = game_state
        self.board = self.game_state.board
        self.has_moved = False

    def get_legal_moves(self, row, col, moves):
        row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.game_state.white_to_move else "b"

        for i in range(8):
            end_row = row + row_moves[i]
            end_col = col + col_moves[i]

            if 0 <= end_row <= 7 and 0 <= end_col <= 7:
                end_piece = self.board[end_row][end_col]

                if end_piece[0] != ally_color:
                    self.update_location(ally_color, end_col, end_row, moves, row, col)

    def update_location(self, ally_color, end_col, end_row, moves, row, col):
        if ally_color == "w":
            self.game_state.white_king_location = (end_row, end_col)
        else:
            self.game_state.black_king_location = (end_row, end_col)

        in_check, pins, checks = self.game_state.check_for_pins()

        if not in_check:
            moves.append(Move((row, col), (end_row, end_col), self.board, can_castle=True))

        if ally_color == "w":
            self.game_state.white_king_location = (row, col)
        else:
            self.game_state.black_king_location = (row, col)
