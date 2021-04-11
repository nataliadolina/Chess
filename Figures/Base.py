from math import sqrt


class Figure:
    start_cell = [0, 0]
    row, col = None, None
    color = ""
    name = ""
    full_name = ""
    dir = 1
    board = None

    def __init__(self, row, col, board, color):
        self.board = board
        self.color_names = {"w": "бел", "b": "чёрн"}
        self.start_cell = (row, col)
        self.color = color
        self.nums_moves = 0

        self.row = row
        self.col = col

        self.set_name()
        if color == "b":
            self.name = self.name.lower()
            self.dir = -1

        elif color == "w":
            self.name = self.name.upper()
            self.dir = 1

        self.board.set_cell(row, col, self)
        self.board.add_figure(self)

    def get_fullname(self):
        return self.full_name

    def set_pos(self, row, col):
        self.row, self.col = row, col

    def get_name(self):
        return self.name

    def set_name(self):
        pass

    def get_available_cells(self):
        moves, attacks = self.get_possible_moves(), self.get_possible_attacks()
        return list(set(moves + attacks)), moves, attacks

    def get_possible_moves(self):
        return []

    def get_possible_attacks(self):
        return []

    def make_move(self, row, col, change=False, sender=None):
        took = self.make_take(row, col)
        if took and sender:
            sender.set_popped_figure(took)
            return True
        cells, moves, attacks = self.get_available_cells()
        if (row, col) in cells or change:
            popped = self.board.pop_figure(row, col)
            if popped:
                if change:
                    return False
                sender.set_popped_figure(popped)
                print(f"Фигура {popped.get_fullname()} выбыла из игры.")

            self.set_take(row)
            self.board.set_cell(row, col, self)
            self.board.set_cell(self.row, self.col, EmptyCell())
            self.row, self.col = row, col
            return True
        return False

    def change_nums_moves(self, step):
        self.nums_moves += step

    def set_take(self, row):
        pass

    def make_take(self, row, col):
        return False

    def if_has_moved(self):
        return self.nums_moves != 0

    def need_to_append(self, cell):
        if not cell or type(cell) == str:
            return False

        if cell.get_name() == ".":
            return True

        try:
            if self.board.is_figure(cell):
                if cell.get_color == self.color:
                    return False

        except Exception as e:
            return True

        return True

    def del_access(self, cells, for_attacks=False):
        delete = []
        for row, col in cells:
            cell = self.board.get_cell(row, col)
            if not self.need_to_append(cell):
                delete.append((row, col))
                continue

            if not for_attacks:
                if cell.get_name() != ".":
                    delete.append((row, col))
            else:
                if self.board.is_figure(cell):
                    if cell.get_color() == self.color:
                        delete.append((row, col))
                else:
                    delete.append((row, col))

        return list(set(cells).difference(set(delete)))

    def get_pos(self):
        return self.row, self.col

    def get_color(self):
        return self.color

    def get_board(self):
        return self.board


class LongwayFigure(Figure):
    def __init__(self, row, col, board, color="w"):
        super().__init__(row, col, board, color)

    def split_by_plus(self, moves):
        row_left = []
        row_right = []
        col_up = []
        col_down = []

        for cell in moves:
            row, col = cell
            if col < self.col and row == self.row:
                row_left.append((row, col))

            elif col > self.col and row == self.row:
                row_right.append((row, col))

            elif row < self.row and col == self.col:
                col_up.append((row, col))

            elif row > self.row and col == self.col:
                col_down.append((row, col))

        return {"left": row_left, "right": row_right, "up": col_up, "down": col_down}

    def split_by_x(self, moves):
        b = {"up_left": [], "up_right": [], "down_left": [], "down_right": []}
        for cell in moves:
            row, col = cell
            if row > self.row:
                if col < self.col:
                    b["up_left"].append(cell)
                elif col > self.col:
                    b["up_right"].append(cell)

            elif row < self.row:
                if col < self.col:
                    b["down_left"].append(cell)
                elif col > self.col:
                    b["down_right"].append(cell)
        return b

    def get_plus(self):
        moves = []
        for i in range(1, 9):
            cell = self.board.get_cell(i, self.col)
            if not self.need_to_append(cell):
                break

            else:
                moves.append((i, self.col))

        for i in range(1, 9):
            cell = self.board.get_cell(self.row, i)
            if not self.need_to_append(cell):
                break

            else:
                moves.append((self.row, i))

        return moves

    def get_cross(self):
        moves = []
        o = self.row - self.col
        offset = o
        if o <= 0:
            offset = - o
            row, col = 1, offset + 1

        else:
            row, col = offset + 1, 1

        while self.board.get_cell(row, col):
            cell = self.board.get_cell(row, col)
            if not self.need_to_append(cell):
                break

            else:
                moves.append((row, col))
                row, col = row + 1, col + 1
        o = self.row + self.col
        if o <= 9:
            offset = 9 - o
            row, col = 1, 8 - offset

        else:
            row, col = o - 8, 8

        while self.board.get_cell(row, col):
            cell = self.board.get_cell(row, col)
            if not self.need_to_append(cell):
                break

            else:
                moves.append((row, col))
                row, col = row + 1, col - 1

        return moves

    def del_access(self, cells, for_attacks=False):
        delete = []
        cells.sort(key=lambda x: sqrt((self.row - x[0]) ** 2 + (self.col - x[1]) ** 2))
        for i in range(len(cells)):
            row, col = cells[i]
            cell = self.board.get_cell(row, col)
            if not cell:
                delete.append(cells[i])
            else:
                if not for_attacks:
                    if cell.get_name() != ".":
                        delete += cells[i:]
                        break

                else:
                    if cell.get_name() == ".":
                        delete.append(cells[i])

                    elif self.board.is_figure(cell):
                        if cell.get_color() == self.color:
                            delete += cells[i:]
                            break
                        else:
                            try:
                                delete += cells[i + 1:]

                            except IndexError:
                                delete.append(cells[i])

                            finally:
                                break
        result = set(cells).difference(set(delete))
        return list(result)

    def get(self, for_attacks=False, *operations):
        moves = []
        for op in operations:
            b = {**self.split_by_x(op()), **self.split_by_plus(op())}
            for key in b.keys():
                m = self.del_access(b[key], for_attacks)
                if m:
                    moves += m
        return moves


class EmptyCell:
    def __init__(self):
        self.name = "."
        self.take = False

    def set_take(self, value):
        self.take = value

    def get_take(self):
        return self.take

    def get_name(self):
        return self.name
