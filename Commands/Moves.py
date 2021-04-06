class MoveFigure:
    def __init__(self, figure, row, col, change=False):
        self.aim_row = row
        self.aim_col = col
        self.figure = figure
        self.change = change

    def execute(self):
        return self.figure.make_move(self.aim_row, self.aim_col, self.change)

    def display_data(self):
        print(self.figure, self.aim_row, self.aim_col)


class MovesContainer:
    def __init__(self, *moves):
        self.commands = moves

    def execute(self):
        for command in self.commands:
            res = command.execute()
            if not res:
                return res
        return True
