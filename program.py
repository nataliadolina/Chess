from board import board
from Figures import Pawn, King, Queen, Rook, Bishop, Knight
from Readers.full_notation import FullNoteReader
from Readers.short_notation import ShortNoteReader
from Readers.manual_input import ManualInputReader

cells = {"8": 1, "7": 2, "6": 3, "5": 4, "4": 5, "3": 6, "2": 7, "1": 8, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6,
         "G": 7, "H": 8}

for row in range(7, 8):
    for col in range(1, 9):
        p = Pawn.Pawn(row, col, board)

for row in range(2, 3):
    for col in range(1, 9):
        p = Pawn.Pawn(row, col, board, "b")

r1_w = Rook.Rook(8, 1, board)
r2_w = Rook.Rook(8, 8, board)

r1_b = Rook.Rook(1, 1, board, "b")
r2_b = Rook.Rook(1, 8, board, "b")

n1_w = Knight.Knight(8, 2, board)
n2_w = Knight.Knight(8, 7, board)

n1_b = Knight.Knight(1, 2, board, "b")
n2_b = Knight.Knight(1, 7, board, "b")

b1_w = Bishop.Bishop(8, 3, board)
b2_w = Bishop.Bishop(8, 6, board)

b1_b = Bishop.Bishop(1, 3, board, "b")
b2_b = Bishop.Bishop(1, 6, board, "b")

q_b = Queen.Queen(1, 4, board, "b")
q_w = Queen.Queen(8, 4, board)

k_b = King.King(1, 5, board, "b")
k_w = King.King(8, 5, board)

board.display_board()
colors = ["белых", "чёрных"]
current = 0
modes = ["1. Ввод вручную", "2. Полная нотация(из файла)", "3. Краткая нотация(из файла)"]
print("\n".join(modes))
print("Пожалуйста, выберете из предложенных вариантов режим, в котором вы хотите играть\n"
      "Вы сможете изменить режим в любой момент, введя другую цифру.")

regime = input()
while regime not in ["1", "2", "3"]:
    regime = input("Недоступный режим. Попробуйте ещё раз.")

regime = int(regime)
regimes = {1: ManualInputReader, 2: FullNoteReader, 3: ShortNoteReader}
func = regimes[regime](board)
func1 = ShortNoteReader(board)
func1.set_file("chess_parts/short/part1")
func1.get_data()
current_file = "chess_parts/"


def get_file():
    global current_file
    file = current_file
    found = False
    while not found:
        file += input("Введите путь до файла относительно chess_parts/")
        try:
            open(file)

        except FileNotFoundError:
            print("Файла не существует. Введите путь до файла ещё раз.")

        else:
            found = True

    return file


def save_to_file(name):
    path = f"chess_parts/full/{name}"
    s = ""
    k = 0
    for i in range(0, len(commands_storage) - 1, 2):
        k += 1
        pair = str(k) + "." + commands_storage[i].get_full_note_view() + " " + commands_storage[
            i + 1].get_full_note_view() + "\n"
        s += pair

    with open(path, 'wt') as f:
        f.write(s)


if regime in [2, 3]:
    current_file = get_file()
    func.set_file(current_file)

commands_storage = []
current_color = "w"
prev_func = None
while len(board.get_specific_figures("k", "w")) > 0 and len(board.get_specific_figures("k", "b")) > 0:
    res_inp = func.input_data()
    if res_inp == "stop":
        commands_storage += func.get_executed()
        need_to_save = input("Хотите сохранить разыгранную партию в  файл? Пожалуйста, введите да или нет.").lower()
        while need_to_save not in ["да", "нет"]:
            need_to_save = input("Хотите сохранить разыгранную партию в  файл? Пожалуйста, введите да или нет.").lower()

        if need_to_save == "да":
            file_name = input("Введите название файла. В файл с таким названием будет сохранена ваша партия.")
            save_to_file(file_name)
            print(f"Готово! Файл с вашей партией, записанной в полной нотации, \n"
                  f" находится по адресу chess_parts/full/{file_name}")
        break

    while not res_inp or type(res_inp) == int:
        print(res_inp)
        if res_inp == 1:
            prev_func = func
            func = regimes[int(res_inp)](board)
            func.change_color_query(prev_func.get_current_color())
            print("Смена режима прошла успешно!")
            commands_storage += prev_func.get_executed()
        res_inp = func.input_data()
    func.execute()

print("Ввод прерван по просьбе игроков.")
