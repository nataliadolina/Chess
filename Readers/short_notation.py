from Commands.Moves import MovesContainer
from Commands.Moves import MoveFigure
from .ReaderBase import FileReaderBase


class ShortNoteReader(FileReaderBase):
    def __init__(self, board):
        super().__init__(board)
        self.file = None

    def get_data(self):
        def get_cells(r_file):
            s = r_file.read().split()
            return [i for i in s if i[-1] != "."]

        with open(self.file, mode="r", encoding="utf-8") as r_file:
            return get_cells(r_file)

    def get_move(self, cell):
        def convert_to_num_cell(cell_name):
            cell1 = cell_name[:]
            cell1 = "".join(filter(lambda x: x.isalpha() or x.isdigit(), list(cell1)))
            c, r = cell1[len(cell1) - 2:]
            return self.cells[r], self.cells[c.upper()]

        current_color = self.get_current_color()
        if cell == "O-O" or cell == "O-O-O":
            k = self.board.get_specific_figures("k", current_color)[0]
            castle = k.castling(cell)
            castle.set_full_note_view(cell)
            return castle

        figures = []
        if len(cell) > 2 and cell[0].upper() == cell[0]:
            figures = self.board.get_specific_figures(cell[0].lower(), current_color)
            cell = cell[1:]
        elif len(cell) == 2 or len(cell) > 2 and cell[0].lower() == cell[0]:
            figures = self.board.get_specific_figures("p", current_color)
        try:
            moves_figures = {i: i.get_possible_moves() for i in figures}
            attacks_figures = {i: i.get_possible_attacks() for i in figures}

        except TypeError:
            return False

        finish = convert_to_num_cell(cell)
        if "x" not in cell:
            try:
                figure_to_move = [_[0] for _ in moves_figures.items() if finish in _[1]]

            except IndexError:
                return False

        else:
            try:
                figure_to_move = [_[0] for _ in attacks_figures.items() if finish in _[1]]

            except Exception:
                return False
        if len(figure_to_move) > 1 and cell[0].lower() == cell[0] and len(cell) > 2:
            figure_to_move = [f for f in figure_to_move if f.get_pos()[1] == self.cells[cell[0].upper()]]
            if len(figure_to_move) != 1:
                return False

        figure_to_move = figure_to_move[0]
        return MovesContainer(MoveFigure(figure_to_move, finish[0], finish[1]))
