from .Base import Figure
from ..program import color_names


class Knight(Figure):
    def __init__(self, row, col, color="w"):
        super().__init__(row, col, color)

    def set_name(self):
        self.name = "n"
        self.full_name = color_names[self.color] + "ый" + " конь"

    def get_moves(self):
        moves = [(self.row + 2, self.col + 1), (self.row + 2, self.col - 1), (self.row - 2, self.col + 1),
                 (self.row - 2, self.col - 1), (self.row + 1, self.col + 2), (self.row + 1, self.col - 2),
                 (self.row - 1, self.col + 2), (self.row - 1, self.col - 2)]

        return moves

    def get_possible_moves(self):
        return self.del_access(self.get_moves())

    def get_possible_attacks(self):
        return self.del_access(self.get_moves(), True)
