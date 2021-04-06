from ..board import board
from .Base import Figure
from ..program import color_names


class Pawn(Figure):
    def __init__(self, row, col, color="w"):
        super().__init__(row, col, color)

    def set_name(self):
        self.name = "p"
        self.full_name = color_names[self.color] + "ая" + " пешка"

    def set_take(self, row):
        if abs(row - self.row) == 2:
            empty_cell = board.get_cell(self.row - self.dir, self.col)
            empty_cell.set_take(True)

    def get_possible_moves(self):
        moves = [(self.row - 1 * self.dir, self.col)]
        if not self.has_moved:
            moves.append((self.row - 2 * self.dir, self.col))
        moves = self.del_access(moves)
        return moves

    def get_attacks(self):
        return [(self.row - self.dir, self.col + 1), (self.row - self.dir, self.col - 1)]

    def make_take(self, row, col):
        takes = self.get_takes()
        if not takes:
            return False
        coords = [i[0] for i in takes.items()][0]
        f_coords = [i[1] for i in takes.items()][0]
        if (row, col) == coords:
            board.pop_figure(f_coords[0], f_coords[1])
            return True
        return False

    def get_takes(self):
        co = {"w": "b", "b": "w"}
        attacks = self.get_attacks()
        for a in attacks:
            c = board.get_cell(a[0], a[1])
            if self.need_to_append(c):
                if c.get_name == ".":
                    if c.get_take():
                        pawns = board.get_specific_figures("p", co[self.color])
                        pawn = [f for f in pawns if f.get_pos()[0] == self.row and f.get_pos()[1] == a[1]]
                        if (self.color == "w" and self.row == 4 or self.color == "b" and self.row == 5) and pawn:
                            return {a: pawn.get_pos()}

        return None

    def get_possible_attacks(self):
        attacks = self.get_attacks()
        attacks = self.del_access(attacks, True)
        return attacks
