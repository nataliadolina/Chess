from .Base import LongwayFigure
from ..program import color_names


class Rook(LongwayFigure):
    def __init__(self, row, col, color="w"):
        super().__init__(row, col, color)

    def set_name(self):
        self.name = "r"
        self.full_name = color_names[self.color] + "ая" + " ладья"

    def get_possible_moves(self):
        return self.get(False, self.get_plus)

    def get_possible_attacks(self):
        return self.get(True, self.get_plus)
