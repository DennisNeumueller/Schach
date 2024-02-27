import Move

class Bishop:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_legal_moves(self, row, col, moves):
        piece_pinned, pin_direction = self.check_pinned_piece(row, col)

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))
        enemy_color = "b" if self.game_state.white_to_move else "w"

        for direction in directions:
            for i in range(1, 8):
                end_row, end_col = row + direction[0] * i, col + direction[1] * i
                if not (end_row <= 7 and end_col <= 7):
                    break  # Off the board
                if not piece_pinned or pin_direction == direction or pin_direction == (-direction[0], -direction[1]):
                    end_piece = self.game_state.board[end_row][end_col]
                    if end_piece == "--":
                        moves.append(Move.Move((row, col), (end_row, end_col), self.game_state.board))
                    elif end_piece[0] == enemy_color:
                        moves.append(Move.Move((row, col), (end_row, end_col), self.game_state.board))
                        break
                    else:
                        break
        return moves

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
