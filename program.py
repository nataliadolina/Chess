from .board import board
from .Figures import Pawn, King, Queen, Rook, Bishop, Knight

cells = {"8": 1, "7": 2, "6": 3, "5": 4, "4": 5, "3": 6, "2": 7, "1": 8, "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6,
         "G": 7, "H": 8}

color_names = {"w": "бел", "b": "чёрн"}

for row in range(7, 8):
    for col in range(1, 9):
        p = Pawn.Pawn(row, col, "w")

for row in range(2, 3):
    for col in range(1, 9):
        p = Pawn.Pawn(row, col, "b")

r1_w = Rook.Rook(8, 1)
r2_w = Rook.Rook(8, 8)

r1_b = Rook.Rook(1, 1, "b")
r2_b = Rook.Rook(1, 8, "b")

n1_w = Knight.Knight(8, 2)
n2_w = Knight.Knight(8, 7)

n1_b = Knight.Knight(1, 2, "b")
n2_b = Knight.Knight(1, 7, "b")

b1_w = Bishop.Bishop(8, 3)
b2_w = Bishop.Bishop(8, 6)

b1_b = Bishop.Bishop(1, 3, "b")
b2_b = Bishop.Bishop(1, 6, "b")

q_b = Queen.Queen(1, 4, "b")
q_w = Queen.Queen(8, 4)

k_b = King.King(1, 5, "b")
k_w = King.King(8, 5)

board.display_board()

current = 0
colors = ["белых", "чёрных"]
color1 = ["белые", "чёрные"]
b_color = {"белых": "w", "чёрных": "b"}


# print(file_reader("tt.txt"))


def move(input):
    start, finish = input.split()
    move = False
    try:
        cell = board.get_cell(cells[start[1]], cells[start[0].upper()])
        row, col = cells[finish[1]], cells[finish[0].upper()]
        move = cell.make_move(row, col)
    except Exception:
        pass

    if not move:
        print("Некорректный ход. Пожалуйста попробуйте ещё раз.")
        return False

    return True


while board.contains_two_kings():
    inp = input(f"Ход {colors[current]}: ")
    moved = move(inp)
    while not moved:
        inp = input(f"Ход {colors[current]}: ")
        moved = move(inp)
    current += 1
    current %= 2
    board.display_board()

print(f"{color1[current].capitalize()} выиграли!")
