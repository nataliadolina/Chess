class ReaderBase:
    def __init__(self, board):
        self.board = board
        self.cur_cursor = 0
        self.cursor = 0
        self.data = []
        self.executed = []

        self.c = {"w": "белых", "b": "чёрных"}
        self.cells = {"8": 1, "7": 2, "6": 3, "5": 4, "4": 5, "3": 6, "2": 7, "1": 8, "A": 1, "B": 2, "C": 3, "D": 4,
                      "E": 5, "F": 6, "G": 7, "H": 8}

    def change_color_query(self, first):
        s = {"w", "b"}
        second = list(s.difference(first))[0]
        self.c = {first: self.c[first], second: self.c[second]}

    def get_current_color(self):
        c = list(self.c.keys())
        return c[self.cur_cursor % 2]

    def get_move(self, cell):
        pass

    def input_data(self):
        pass

    def get_data(self):
        pass

    def get_executed(self):
        return self.executed

    def change_cursor(self, value):
        aim_cursor = self.cur_cursor + value
        if aim_cursor < 0 or aim_cursor > len(self.data):
            print(f"Курсор не входит в рамки данных файла. \n"
                  f" В наcтоящее время курсор стоит на {str(self.cur_cursor)}ой команде.\n Вы можете двигать курсор"
                  f" в диапазоне от 0 до {len(self.data)}.")
            return False
        self.cursor = aim_cursor
        return True

    def execute(self):
        c = {"w": "Белые", "b": "Чёрные"}
        r_c = {"b": "Белые", "w": "Чёрные"}
        if self.cur_cursor < self.cursor:
            while self.cur_cursor != self.cursor:
                data = self.data[self.cur_cursor]
                move = self.get_move(data)
                move.do()
                if move.get_commands_count() != 2:
                    move.set_full_note_view()
                print(f"{c[self.get_current_color()]} сходили.")
                self.board.display_board(color=self.get_current_color(), instruction=move.get_instruction())
                self.executed.append(move)
                self.cur_cursor += 1

        elif self.cur_cursor > self.cursor:
            while self.cur_cursor != self.cursor:
                self.executed[self.cur_cursor - 1].undo()
                # self.change_color_query(self.get_current_color())
                print(f"{r_c[self.get_current_color()]} отменили ход.")
                self.board.display_board(color=self.get_current_color(),
                                         instruction=self.executed[self.cur_cursor - 1].get_instruction())
                self.cur_cursor -= 1
                self.executed.pop(self.cur_cursor)


class FileReaderBase(ReaderBase):
    def __init__(self, board):
        super().__init__(board)
        self.file = None

    def get_data(self):
        pass

    def input_data(self):
        data = input(
            f"Введите один знак или комбинацию знаков из > и < или переключитесь на мануальный режим (введите 1)")
        if data == "1":
            return int(data)

        data = "".join(list(filter(lambda x: x == ">" or x == "<", list(data))))
        if data == "":
            print("Некорректный ввод. Вы можете вводить только знаки <, > или номер режима 1")
            return False

        return self.change_cursor(data.count(">") - data.count("<"))

    def set_file(self, filename):
        self.file = filename
        self.data = self.get_data()
