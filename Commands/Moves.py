class Command:
    def do(self):
        pass

    def undo(self):
        pass


class MoveFigure(Command):
    def __init__(self, figure, row, col, change=False):
        self.row, self.col = figure.get_pos()
        self.aim_row = row
        self.aim_col = col
        self.figure = figure
        self.change = change

        self.popped = None
        self.p_row, self.p_col = None, None

    def do(self):
        res = self.figure.make_move(self.aim_row, self.aim_col, self.change, self)
        if res:
            self.figure.change_nums_moves(1)
        return res

    def set_popped_figure(self, figure):
        self.popped = figure
        print(figure.get_color())
        self.p_row, self.p_col = figure.get_pos()
        print("____POPPED FIGURE SETTED____", self.popped, self.p_row, self.p_col)

    def undo(self):
        self.figure.make_move(self.row, self.col, True)
        self.figure.change_nums_moves(-1)
        if self.popped:
            self.figure.get_board().set_cell(self.p_row, self.p_col, self.popped)

    def display_data(self):
        print(self.figure, self.aim_row, self.aim_col)


class MovesContainer:
    def __init__(self, *moves):
        self.commands = moves

    def do(self):
        for command in self.commands:
            res = command.do()
            if not res:
                return res
        return True

    def undo(self):
        for i in range(len(self.commands) - 1, -1, -1):
            self.commands[i].undo()
