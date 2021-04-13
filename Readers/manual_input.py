from Commands.Moves import MovesContainer
from Commands.Moves import MoveFigure
from .ReaderBase import ReaderBase


class ManualInputReader(ReaderBase):
    def __init__(self, board):
        super().__init__(board)

    def convert_to_num_cell(self, cell):
        try:
            row, col = self.cells[cell[1]], self.cells[cell[0].upper()]

        except KeyError and IndexError:
            print("Несуществующая клетка.")
            return None

        else:
            return row, col

    def get_figure(self, row, col):
        cell = self.board.get_cell(row, col)
        if not cell:
            print("Ошибка. Не получилось расшифровать.")
            return None
        if self.board.is_figure(cell):
            if cell.get_color() == self.get_current_color():
                return cell
            else:
                print("Произошла ошибка. Вы обратились к фигуре соперника.")
                return None
        else:
            print("Ошибка. Вы ввели координаты пустой клетки.")
            return None

    def get_move(self, cell):
        return cell

    def input_data(self):
        move_figure = None
        while not move_figure:
            start_cell = input("Пожалуйста, введите координаты движущйся фигуры.")
            coords = self.convert_to_num_cell(start_cell)
            if not coords:
                continue
            row, col = coords
            move_figure = self.get_figure(row, col)

        aim_move = None
        while not aim_move:
            finish_cell = input("Пожалуйста, введите координаты целевой клетки.")
            coords = self.convert_to_num_cell(finish_cell)
            if not coords:
                continue

            if coords in move_figure.get_available_cells()[0]:
                row, col = coords
                aim_move = MovesContainer(MoveFigure(move_figure, row, col))

            else:
                print("Выбранная Вами фигура не может ходить на эту клетку. \n Выберете одну из выделенных клеток.")
        self.data.append(aim_move)
        self.cursor += 1
        return aim_move
