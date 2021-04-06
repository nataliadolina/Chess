from ..board import board
from ..Commands.Moves import MovesContainer
from ..Commands.Moves import MoveFigure
from ..program import cells


def file_reader(file):
    moves = []

    def get_moves(row):
        current_color = "b"
        local_moves = []
        row = row.split()
        for j in range(len(row)):

            el = row[j]
            el = el.replace("+", "")
            if True not in list(map(lambda x: x.isalpha(), el)):
                continue

            else:
                if current_color == "b":
                    current_color = "w"

                else:
                    current_color = "b"

                if el == "O-O" or el == "O-O-O":
                    k = board.get_specific_figures("k", current_color)[0]
                    move = k.castling(el)
                    if move:
                        local_moves.append(move)
                        local_moves[-1].execute()
                        continue
                else:

                    figures = []
                    if len(el) > 2 and el != "O-O":
                        figures = board.get_specific_figures(el[0].lower(), current_color)
                    elif len(el) == 2:
                        figures = board.get_specific_figures("p", current_color)
                    try:
                        moves_figures = {i: i.get_possible_moves() for i in figures}
                        attacks_figures = {i: i.get_possible_attacks() for i in figures}

                    except TypeError:
                        print(el, figures)
                        return None

                    c, r = el[len(el) - 2:]
                    finish = (cells[r], cells[c.upper()])
                    figure_to_move = None
                    if "x" not in el:
                        try:
                            figure_to_move = [_[0] for _ in moves_figures.items() if finish in _[1]]
                            print(current_color, figure_to_move)
                        except IndexError:
                            print(current_color, figure_to_move, c, r)
                            return None

                    else:
                        try:
                            figure_to_move = [_[0] for _ in attacks_figures.items() if finish in _[1]][0]

                        except Exception:
                            print("Ошибка", el)
                            return None
                    try:
                        local_moves.append(MovesContainer(MoveFigure(figure_to_move[0], finish[0], finish[1])))
                        local_moves[-1].execute()
                    except:
                        print(el)
                    board.display_board()

        return local_moves

    with open(file, mode="r", encoding="utf-8") as r_file:
        for row in r_file:
            moves += get_moves(row.strip())
    return moves
