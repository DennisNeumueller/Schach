import Move

class Pawn():
    def __init__(self, game_state):
        self.game_state = game_state

    def get_legal_moves(self, row, col, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.game_state.pins) - 1, -1, -1):
            if self.game_state.pins[i][0] == row and self.game_state.pins[i][1] == col:
                piece_pinned = True
                pin_direction = (self.game_state.pins[i][2], self.game_state.pins[i][3])
                self.game_state.pins.remove(self.game_state.pins[i])
                break

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

        if self.game_state.board[row + move_amount][col] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move.Move((row, col), (row + move_amount, col), self.game_state.board))
                if row == start_row and self.game_state.board[row + 2 * move_amount][col] == "--":  # 2 square pawn advance
                    moves.append(Move.Move((row, col), (row + 2 * move_amount, col), self.game_state.board))
        if col - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.game_state.board[row + move_amount][col - 1][0] == enemy_color:
                    moves.append(Move.Move((row, col), (row + move_amount, col - 1), self.game_state.board))
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col - 1)
                            outside_range = range(col + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col, -1)
                            outside_range = range(col - 2, -1, -1)
                        for i in inside_range:
                            if self.game_state.board[row][i] != "--":
                                blocking_piece = True
                        for i in outside_range:
                            square = self.game_state.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move.Move((row, col), (row + move_amount, col - 1), self.game_state.board))
        if col + 1 <= 7: #capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.game_state.board[row + move_amount][col + 1][0] == enemy_color:
                    moves.append(Move.Move((row, col), (row + move_amount, col + 1), self.game_state.board))
                    attacking_piece = blocking_piece = False
                    if king_row == row:
                        if king_col < col:
                            inside_range = range(king_col + 1, col)
                            outside_range = range(col + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_col - 1, col + 1, -1)
                            outside_range = range(col - 1, -1, -1)
                        for i in inside_range:
                            if self.game_state.board[row][i] != "--":
                                blocking_piece = True
                        for i in outside_range:
                            square = self.game_state.board[row][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move.Move((row, col), (row + move_amount, col + 1), self.game_state.board))
