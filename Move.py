class Move:
    def __init__(self, start_square, end_square, board, can_castle=False):
        self.start_row = start_square[0]
        self.start_col = start_square[1]
        self.end_row = end_square[0]
        self.end_col = end_square[1]

        # Retrieving information about the pieces involved in the move
        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

        # Checking if the move results in pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_row == 0) or (
                self.piece_moved == "bp" and self.end_row == 7)

        # Checking if the move involves capturing an opponent's piece
        self.is_capture = self.piece_captured != "--"

        self.can_castle = can_castle

        # Unique identifier for the move based on coordinates
        self.moveID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False