from board import board
from program import cells
from Commands.Moves import MovesContainer, MoveFigure


def manual_input(input, current_color):
    b = {"чёрных": "b", "белых": "w"}
    current_color = b[current_color]

    def move(input):
        start, finish = input.split()
        if input == "0-0" or input == "0-0-0":
            king = board.get_specific_figures("k", current_color)[0]
            return king.castling(input)
        try:
            cell = board.get_cell(cells[start[1]], cells[start[0].upper()])
            row, col = cells[finish[1]], cells[finish[0].upper()]
            return MovesContainer(MoveFigure(cell, row, col))

        except Exception:
            return False

    moved = move(input).execute()
    while not moved:
        inp = input(f"Ход {current_color}: ")
        moved = move(inp).execute()

    return moved
