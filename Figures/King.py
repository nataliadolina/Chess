from .Base import Figure
from ..program import color_names
from ..board import board
from ..Commands.Moves import MovesContainer
from ..Commands.Moves import MoveFigure


class King(Figure):
    def __init__(self, row, col, color="w"):
        super().__init__(row, col, color)

    def set_name(self):
        self.name = "k"
        self.full_name = color_names[self.color] + "ый" + " король"

    def get_moves(self):
        moves = [(self.row + 1, self.col + 1), (self.row + 1, self.col - 1), (self.row - 1, self.col + 1),
                 (self.row - 1, self.col - 1), (self.row, self.col + 1), (self.row, self.col - 1),
                 (self.row + 1, self.col), (self.row - 1, self.col)]

        return moves

    def get_possible_moves(self):
        return self.del_access(self.get_moves())

    def get_possible_attacks(self):
        return self.del_access(self.get_moves(), True)

    def under_attack(self, is_mat=False):
        is_under_attack = []
        if not is_mat:
            pos = [self.get_pos()]
        else:
            pos = self.get_available_cells()[0]
        color = self.color
        if color == "w":
            color = "b"
        else:
            color = "w"
        for name in board.get_figures().keys():
            figures = board.get_specific_figures(name, color)
            for f in figures:
                if True in list(filter(lambda p: p in f.get_possible_attacks(), pos)):
                    if not is_mat:
                        return True

                    else:
                        is_under_attack.append(True)
        if is_mat:
            if False not in is_under_attack:
                if board.get_figures_by_color(self.color) == [] or self.under_attack():
                    return True
        return False

    def castling(self, type="0-0", need_to_check=False):
        if self.under_attack() or self.has_moved:
            return None
        rr = [r for r in board.get_specific_figures("r", self.color)]
        for r in rr:
            print(r.if_has_moved())
        rook = [r for r in board.get_specific_figures("r", self.color) if not r.if_has_moved()]

        if not rook:
            return None

        r_short = [r for r in rook if r.get_pos()[1] == 8]
        r_long = [r for r in rook if r.get_pos()[1] == 1]
        if (type == "0-0" or type == "O-O") and r_short != []:
            r = r_short[0]
            if not [f for f in board.get_row(self.row)[6:8] if board.is_figure(f)] or not need_to_check:
                return MovesContainer(MoveFigure(self, self.row, 7, True), MoveFigure(r, self.row, 6, True))

        if r_long != [] and (type == "0-0-0" or type == "O-O-O") or not need_to_check:
            r = r_long[0]
            if not [f for f in board.get_row(self.row)[2:5] if board.is_figure(f)]:
                return MovesContainer(MoveFigure(self, self.row, 3, True), MoveFigure(r, self.row, 4, True))

        return None
