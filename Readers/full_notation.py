from Commands.Moves import MovesContainer
from Commands.Moves import MoveFigure
from .ReaderBase import ReaderBase


class FullNoteReader(ReaderBase):
    def __init__(self, board):
        super().__init__(board)
        self.file = None

    def get_move(self, cell):

        def convert_to_num_cell(cell_name):
            cell_name = "".join(filter(lambda x: x.isalpha() or x.isdigit(), list(cell_name)))
            cell_name = cell_name[len(cell_name) - 2:]
            return self.cells[cell_name[1]], self.cells[cell_name[0].upper()]

        if cell == "0-0" or cell == "0-0-0":
            king = self.board.get_specific_figures("k", self.get_current_color())[0]
            return king.castling(cell)

        start, finish = None, None
        if "-" in cell:
            start, finish = cell.split("-")

        elif "x" in cell:
            start, finish = cell.split("x")
        r_start, c_start = convert_to_num_cell(start)
        r_fin, c_fin = convert_to_num_cell(finish)
        figure = self.board.get_cell(r_start, c_start)
        return MovesContainer(MoveFigure(figure, r_fin, c_fin))

# moo = FullNoteReader()
# moo.set_file("Chess/chess_parts/full/part6")
