from board import board
from Figures import Pawn, King, Queen, Rook, Bishop, Knight
from Commands.Moves import MovesContainer, MoveFigure

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

current = 0
colors = ["белых", "чёрных"]
color1 = ["белые", "чёрные"]
b_color = {"белых": "w", "чёрных": "b"}


def move(input):
    start, finish = input.split()
    if input == "0-0" or input == "0-0-0":
        king = board.get_specific_figures("k", color1[current])[0]
        return king.castling(input)
    try:
        cell = board.get_cell(cells[start[1]], cells[start[0].upper()])
        row, col = cells[finish[1]], cells[finish[0].upper()]
        return MovesContainer(MoveFigure(cell, row, col))

    except Exception:
        return False


while board.contains_two_kings():
    inp = input(f"Ход {colors[current]}: ")
    moved = move(inp).execute()
    while not moved:
        inp = input(f"Ход {colors[current]}: ")
        moved = move(inp).execute()
    current += 1
    current %= 2
    board.display_board()

print(f"{color1[current].capitalize()} выиграли!")
