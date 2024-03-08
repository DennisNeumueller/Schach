import Move

class Knight:
    def __init__(self, game_state):
        self.game_state = game_state

    def get_legal_moves(self, row, col, moves):
        piece_pinned = self.check_pinned_piece(row, col)

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        ally_color = "w" if self.game_state.white_to_move else "b"

        for move in knight_moves:
            end_row = row + move[0]
            end_col = col + move[1]

            if end_row <= 7 and end_col <= 7 and (not piece_pinned or self.is_pinned_on_direction(row, col, move)):
                end_piece = self.game_state.board[end_row][end_col]

                if end_piece[0] != ally_color:
                    moves.append(Move.Move((row, col), (end_row, end_col), self.game_state.board))

    def check_pinned_piece(self, row, col):
        piece_pinned = False
        for i in range(len(self.game_state.pins) - 1, -1, -1):
            if self.game_state.pins[i][0] == row and self.game_state.pins[i][1] == col:
                piece_pinned = True
                self.game_state.pins.remove(self.game_state.pins[i])
                break
        return piece_pinned

    def is_pinned_on_direction(self, row, col, move):
        pin_direction = (move[0], move[1])

        for pin in self.game_state.pins:
            if pin[0] == row and pin[1] == col and pin[2] == pin_direction[0] and pin[3] == pin_direction[1]:
                return True
        return False
