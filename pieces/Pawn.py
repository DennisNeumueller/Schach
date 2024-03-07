import Move


class Pawn:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_legal_moves(self, row, col, moves):
        # Check if the pawn is pinned by a piece (can only move in a certain direction)
        piece_pinned, pin_direction = self.check_pinned_piece(row, col)

        # Determine movement direction based on the side to move (white or black)
        move_amount, start_row, enemy_color, king_row, king_col = self.determine_move_direction(row)

        # Check for 1-square pawn advance
        self.check_advance_moves(row, col, move_amount, start_row, moves, piece_pinned, pin_direction)

        # Check for captures
        self.check_pawn_captures(row, col, move_amount, enemy_color, moves, piece_pinned, pin_direction)

        return moves  # Return the list of legal moves

    def check_pinned_piece(self, row, col):
        piece_pinned = False
        pin_direction = ()

        # Check if the pawn is pinned by a piece (can only move in a certain direction)
        for i in range(len(self.game_state.pins) - 1, -1, -1):
            if self.game_state.pins[i][0] == row and self.game_state.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.game_state.pins[i][2], self.game_state.pins[i][3])
                self.game_state.pins.remove(self.game_state.pins[i])
                break

        return piece_pinned, pin_direction

    def determine_move_direction(self, row):
        if self.game_state.white_to_move:
            move_amount = -1
            start_row = 6
            enemy_color = "b"
            king_row, king_col = self.game_state.white_king_location
        else:
            move_amount = 1
            start_row = 1
            enemy_color = "w"
            king_row, king_col = self.game_state.black_king_location

        return move_amount, start_row, enemy_color, king_row, king_col

    def check_advance_moves(self, row, col, move_amount, start_row, moves, piece_pinned, pin_direction):
        if 0 <= row + move_amount < 8:  # Check if the destination row is within bounds
            if not piece_pinned or pin_direction == (move_amount, 0):
                if self.game_state.board[row + move_amount][col] == "--":  # 1 square pawn advance
                    moves.append(Move.Move((row, col), (row + move_amount, col), self.game_state.board))
                    if row == start_row and self.game_state.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                        moves.append(Move.Move((row, col), (row + 2 * move_amount, col), self.game_state.board))

    def check_pawn_captures(self, row, col, move_amount, enemy_color, moves, piece_pinned, pin_direction):
        # Check for captures
        for col_offset in [-1, 1]:
            new_col = col + col_offset
            if 0 <= new_col <= 7 and 0 <= row + move_amount < 8:
                if not piece_pinned or pin_direction == (move_amount, col_offset):
                    target_square = self.game_state.board[row + move_amount][new_col]

                    # Capture to the left or right
                    if target_square[0] == enemy_color:
                        moves.append(Move.Move((row, col), (row + move_amount, new_col), self.game_state.board))


