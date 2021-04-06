from .Base import LongwayFigure


class Rook(LongwayFigure):
    def __init__(self, row, col, board, color="w"):
        super().__init__(row, col, board, color)

    def set_name(self):
        self.name = "r"
        self.full_name = self.color_names[self.color] + "ая" + " ладья"

    def get_possible_moves(self):
        return self.get(False, self.get_plus)

    def get_possible_attacks(self):
        return self.get(True, self.get_plus)
