from board import board
import os
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


if regime in [2, 3]:
    current_file = get_file()
    func.set_file(current_file)

commands_storage = []
current_color = "w"
while board.get_specific_figures("k", "w") != [] and board.get_specific_figures("k", "b") != []:
    res_inp = func.input_data()
    while not res_inp or type(res_inp) == int:
        if res_inp in [1, 2, 3]:
            func = regimes[regime](board)
            if res_inp in [2, 3]:
                current_file = get_file()
                func.set_file(current_file)
                func.change_color_query(func.get_current_color())

        res_inp = func.input_data()
    commands_storage += func.execute()
    board.display_board()
