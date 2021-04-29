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
        self.full_notation_view = ""

    def get_full_notation_view(self):
        cells_row = {1: "8", 2: "7", 3: "6", 4: "5", 5: "4", 6: "3", 7: "2", 8: "1"}
        cells_col = {1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H"}
        delemeter = "-"
        name = ''
        start_cell = cells_col[self.col].lower() + cells_row[self.row]
        finish_cell = cells_col[self.aim_col].lower() + cells_row[self.aim_row]
        if self.figure.get_name().lower() != "p":
            name = self.figure.get_name().upper()

        if self.popped:
            delemeter = "x"

        return name + start_cell + delemeter + finish_cell

    def get_start(self):
        return self.row, self.col

    def get_finish(self):
        return self.aim_row, self.aim_col

    def do(self):
        res = self.figure.make_move(self.aim_row, self.aim_col, self.change, self)
        if res:
            self.figure.change_nums_moves(1)
        return res

    def set_popped_figure(self, figure):
        self.popped = figure
        self.p_row, self.p_col = figure.get_pos()

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
        self.full_note_view = ""

    def do(self):
        for command in self.commands:
            res = command.do()
            if not res:
                return res
        return True

    def undo(self):
        for i in range(len(self.commands) - 1, -1, -1):
            self.commands[i].undo()

    def set_full_note_view(self, view=""):
        r = {"0-0": "0-0", "O-O": "0-0", "O-O-O": "0-0-0", "0-0-0": "0-0-0"}
        if view == "":
            for command in self.commands:
                self.full_note_view += command.get_full_notation_view()

        else:
            self.full_note_view = r[view]

    def get_full_note_view(self):
        return self.full_note_view

    def get_commands_count(self):
        return len(self.commands)

    def get_instruction(self):
        instruction = []
        for command in self.commands:
            instruction.append((command.get_start(), command.get_finish()))
        return instruction
