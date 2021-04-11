class ReaderBase:
    def __init__(self, board):
        self.board = board
        self.cur_cursor = 0
        self.cursor = 0
        self.data = []
        self.executed = []

        self.c = {"w": "белых", "b": "чёрных"}
        self.cells = {"8": 1, "7": 2, "6": 3, "5": 4, "4": 5, "3": 6, "2": 7, "1": 8, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5,
                 "F": 6, "G": 7, "H": 8}

    def get_data(self):
        def get_cells(r_file):
            s = r_file.read().split()
            return [i[i.index(".") + 1:] if s.index(i) % 2 == 0 else i for i in s]

        with open(self.file, mode="r", encoding="utf-8") as r_file:
            print(get_cells(r_file))
            return get_cells(r_file)

    def get_current_color(self):
        c = list(self.c.keys())
        return c[self.cur_cursor % 2]

    def input_data(self):
        data = input(f"Ход {self.c[self.get_current_color()]}:")
        if data in ["1", "2", "3"]:
            return int(data)

        data = "".join(list(filter(lambda x: x == ">" or x == "<", list(data))))
        if data == "":
            print("Некорректный ввод. Вы можете вводить только знаки <, > или номер режима (1, 2, 3)")
            return False

        self.cursor += data.count(">") - data.count("<")
        print(self.cursor)
        if self.cursor < 0 or self.cursor > len(self.data):
            print(f"Курсор не входит в рамки данных файла. \n"
                  f" В наcтоящее время курсор стоит на {str(self.cur_cursor)}ой команде.\n Вы можете двигать курсор"
                  f" в диапазоне от 0 до {len(self.data)-1}.")
            return False
        return True

    def execute(self):
        arr = []
        if self.cur_cursor < self.cursor:
            while self.cur_cursor != self.cursor:
                data = self.data[self.cur_cursor]
                move = self.get_move(data)
                move.do()
                self.board.display_board()
                arr.append(move)
                self.executed.append(move)
                self.cur_cursor += 1

        elif self.cur_cursor > self.cursor:
            while self.cur_cursor != self.cursor:
                self.cur_cursor -= 1
                self.executed[self.cur_cursor].undo()
                self.executed.pop(self.cur_cursor)

        return arr

    def get_move(self, cell):
        pass

    def change_color_query(self, cur_color):
        s = {"w", "b"}
        second = self.c[cur_color]
        first = list(s.difference(second))[0]
        self.c = {first: self.c[first], second: self.c[second]}

    def set_file(self, filename):
        self.file = filename
        self.data = self.get_data()
