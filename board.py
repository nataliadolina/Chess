from Figures.Base import EmptyCell


class Chess_Board:
    def __init__(self):
        self.field = [[EmptyCell() for i in range(10)] for j in range(10)]
        self.fill_board()
        self.figures = {"p": [], "r": [], "b": [], "n": [], "k": [], "q": []}
        self.popped_figures = []

    def fill_board(self):
        indexes = [0, 9]
        data = list(range(8, 0, -1))
        data.append(".")
        col = [EmptyCell()] * 10
        for i in indexes:
            for j in range(1, 10):
                col[j] = str(data[j - 1])
            self.set_col(i, col)

        for i in indexes:
            row = self.get_row(i)
            data = " ABCDEFGH "
            for j in range(len(row)):
                row[j] = data[j]
            self.set_row(i, row)

    def delete_take(self):
        for row in range(1, 9):
            for col in range(1, 9):
                el = self.field[row][col]
                if el.get_name() == ".":
                    if el.get_take():
                        self.field[row][col].set_take(False)

    def add_figure(self, figure):
        self.figures[figure.get_name().lower()].append(figure)

    def get_popped(self):
        return self.popped_figures

    def get_figures(self):
        return self.figures

    def get_specific_figures(self, name, color):
        try:
            return list(filter(lambda x: x.get_color() == color, self.figures[name]))
        except KeyError:
            print(name, color)

    def is_figure(self, cell):
        try:
            cell.get_fullname()

        except Exception:
            return False
        else:
            return True

    def get_figures_by_color(self, color):
        res = []
        for key in self.figures.keys():
            res += self.get_specific_figures(key, color)
        return res

    def pop_figure(self, row, col):
        f = self.get_cell(row, col)
        if f.get_name() == ".":
            return None
        self.popped_figures.append(f)
        self.field[row][col] = EmptyCell()
        return f

    def get_col(self, offset):
        return self.field[:, offset]

    def set_col(self, offset, value):
        for i in range(10):
            self.field[i][offset] = value[i]

    def get_row(self, offset):
        return self.field[offset]

    def set_row(self, offset, value):
        self.field[offset] = value

    def set_cell(self, row, col, value):
        self.field[row][col] = value

    def get_cell(self, row, col):
        c = None
        try:
            c = self.field[row][col]
        except IndexError:
            return None
        finally:
            if row == 9 or row == 0 or col == 0 or col == 9:
                return None
            return c

    def contains_two_kings(self):
        counter = 0
        for row in self.field:
            for cell in row:
                try:
                    if cell.get_name().lower() == "k":
                        counter += 1
                except Exception:
                    pass

        if counter == 2:
            return True

        return False

    def display_board(self):
        for row in self.field:
            for col in row:
                if type(col) != str:
                    cell = col.get_name()

                else:
                    cell = col
                print("%4s" % cell, end="")
            print()

    def get_board(self):
        return self.field


board = Chess_Board()
