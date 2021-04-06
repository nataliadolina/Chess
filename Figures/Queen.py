from .Base import LongwayFigure
from ..program import color_names


class Queen(LongwayFigure):
    def __init__(self, row, col, color="w"):
        super().__init__(row, col, color)

    def set_name(self):
        self.name = "q"
        self.full_name = color_names[self.color] + "ая" + " королева"

    def get_possible_moves(self):
        return self.get(False, self.get_plus, self.get_cross)

    def get_possible_attacks(self):
        return self.get(True, self.get_plus, self.get_cross)
