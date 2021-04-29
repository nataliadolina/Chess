from Commands.Moves import MovesContainer
from Commands.Moves import MoveFigure
from .ReaderBase import FileReaderBase


class FullNoteReader(FileReaderBase):
    def __init__(self, board):
        super().__init__(board)

    @staticmethod
    def get_regime_name():
        return "2 - полная нотация(из файла)"

    def get_data(self):
        def get_cells(r_file):
            s = r_file.read().split()
            print(s)
            return [i[i.index(".") + 1:] if s.index(i) % 2 == 0 else i for i in s]

        with open(self.file, mode="r", encoding="utf-8") as r_file:
            return get_cells(r_file)

    def get_move(self, cell):

        def convert_to_num_cell(cell_name):
            cell_name = "".join(filter(lambda x: x.isalpha() or x.isdigit(), list(cell_name)))
            cell_name = cell_name[len(cell_name) - 2:]
            return self.cells[cell_name[1]], self.cells[cell_name[0].upper()]

        if cell == "0-0" or cell == "0-0-0":
            king = self.board.get_specific_figures("k", self.get_current_color())[0]
            castle = king.castling(cell)
            castle.set_full_note_view(cell)
            return castle

        start, finish = None, None
        if "-" in cell:
            start, finish = cell.split("-")

        elif "x" in cell:
            start, finish = cell.split("x")
        r_start, c_start = convert_to_num_cell(start)
        r_fin, c_fin = convert_to_num_cell(finish)
        figure = self.board.get_cell(r_start, c_start)
        self.board.display_board()
        return MovesContainer(MoveFigure(figure, r_fin, c_fin))
