from ..board import board
from ..Commands.Moves import MovesContainer
from ..Commands.Moves import MoveFigure
from ..program import cells


def full_notation_reader(filename):
    def get_cells(r_file):
        s = r_file.read().split()
        return [i[i.index(".") + 1:] if s.index(i) % 2 == 0 else i for i in s]

    def get_move(cell, index):
        colors = ['w', "b"]

        def convert_to_num_cell(cell_name):
            global cells
            cell_name = "".join(filter(lambda x: x != "+", list(cell_name)))
            cell_name = cell_name[len(cell_name) - 2:]
            return cells[cell_name[1]], cells[cell_name[0].upper()]

        if cell == "0-0" or cell == "0-0-0":
            king = board.get_specific_figures("k", colors[index % 2])[0]
            return king.castling(cell)

        start, finish = None, None
        if "-" in cell:
            start, finish = cell.split("-")

        elif "x" in cell:
            start, finish = cell.split("x")
        r_start, c_start = convert_to_num_cell(start)
        r_fin, c_fin = convert_to_num_cell(finish)
        figure = board.get_cell(r_start, c_start)
        return MovesContainer(MoveFigure(figure, r_fin, c_fin))

    with open(filename, mode="r", encoding="utf-8") as r_file:
        commands = []
        cells = get_cells(r_file)
        print("__BEGIN___")
        for i in range(len(cells)):
            if i == 123:
                print()
            commands.append(get_move(cells[i], i))
            res = commands[-1].execute()
            board.display_board()
            if not res:
                print(cells[i], i)
                break

        return commands


moo = full_notation_reader("Chess/chess_parts/full/part6")
