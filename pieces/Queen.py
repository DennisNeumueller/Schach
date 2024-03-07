from pieces.Rook import Rook
from pieces.Bishop import Bishop
class Queen():
    def __init__(self, game_state):
        self.game_state = game_state
    def get_legal_moves(self, row, col, moves):
        legal_moves = []

        # Rook Movement
        rook = Rook(self.game_state)
        legal_moves.extend(rook.get_legal_moves(row, col, moves))

        # Bishop Movement
        bishop = Bishop(self.game_state)
        legal_moves.extend(bishop.get_legal_moves(row, col, moves))

