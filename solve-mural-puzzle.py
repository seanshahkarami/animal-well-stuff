"""
Awesome work by the community on collaborating to collect all puzzle pieces!

I took this as my starting point to show how you can just "turn the crank" to find
a possible solution. Haha... I wanted to at least put in some kind of effort towards
solving this!

It turns out there's exactly one, by the way! I thought it'd be interesting if there
was some secret alternative, possibly nonsensical, mural which unlocked something else.
"""

from dataclasses import dataclass

piece_data = """
3301
WYYY
WWYY
YYYY
YYYR

4123
BBBB
BBBB
BBBB
BBBB

0312
WWWW
WRBW
WBYY
WWYY

4103
RBYY
BRYY
YYRY
RYYR

2012
WRWW
RWYW
WWWY
WRWR

2021
YBWW
BRWW
WWWW
WWWW

0221
BWWW
RBWB
RBWB
BRBW

4223
WWWW
WWWW
WWWW
BBWW

2213
WBBB
WBBB
RBBB
RBBB

2221
BBBW
BBRY
BBRY
BBRY


2102
BWWW
WWWW
WWWW
WYYY

0223
WWWW
WWWB
WWBR
WWWB

2131
WRBW
WBWB
WWBW
WWRW

2312
BRBB
WBBB
BBBB
BBBW

3333
BBBB
BBBB
BBBB
BBBB

3414
RWWR
BWWR
BWWR
WWRW

2130
RWYW
RWWR
WRWR
WRWR

1220
RWYW
RWWW
RWWW
RYWW

1302
BBBB
BBBB
BBBB
WWWW

3210
WRWR
WYWR
YYWY
RYYR


2203
BBBB
BBBB
BBBW
WWWW

0110
YBYW
WYWW
WRWW
WRWB

1122
BRWW
WRWB
WRBR
RWWB

0132
WWWW
WWWW
BWYW
RYWW

2241
RWWR
WWWR
WWWR
WWWR

2111
WWWW
WWWW
BWWW
WWWW

4342
WWRW
YWRW
RYYY
BYYY

2233
BBBB
BBBB
BBBB
BBBB

0224
WWWW
WYWW
YBYW
WYWW

3332
BBBB
BBBB
BBBB
BBBB


0432
BBWW
BBWW
BBWW
BWWW

2112
WWRW
YWRW
YYRY
YYYY

1224
WYWR
WRWR
WRWR
WWRW

1303
YBRY
BRBR
RBRY
YRYR

1322
WWWW
WWWB
WWBB
WBBB

3113
WWWW
BBWW
WBBW
RWBB

1142
BBBB
BBBB
BBBB
BBBB

1421
WWBB
BBBB
BBBB
BBBB

3331
RWWW
RWWW
WRWW
WRBB

1201
WBBB
WWBB
YWWB
YYWW


3202
BBBB
BBBB
BBBB
WWWW

0311
WWWW
WWWW
BWWW
WBWW

0023
WWWW
BRWW
YBWW
YWWW

1111
WBYY
WRBR
WWWR
WYWR

1232
WWRW
YYRY
YYYY
YYYY

1021
WWRW
WYRW
YYRY
YRYR

2003
RYRY
YRYR
RYRY
YRYR

1300
YRYB
YYRY
RYYR
YRYY

0141
WWWB
WWWB
WWWB
WWWB

3313
BBBB
BBBB
BBBB
BBBB
"""


@dataclass
class Piece:
    up: int
    right: int
    down: int
    left: int
    colors: list
    used: bool


# load piece data
pieces = []

items = piece_data.split()

while items:
    code = items[0]
    up = int(code[0])
    right = int(code[1])
    down = int(code[2])
    left = int(code[3])
    colors = [list(c) for c in items[1:5]]
    pieces.append(Piece(up, right, down, left, colors, False))
    items = items[5:]


WIDTH = 10
HEIGHT = 5


puzzle = [None] * (WIDTH * HEIGHT)


def get_piece(x, y):
    return puzzle[y * WIDTH + x]


def set_piece(x, y, p):
    puzzle[y * WIDTH + x] = p


def piece_fits(p: Piece, x: int, y: int):
    return (
        piece_fits_left(p, x, y)
        and piece_fits_right(p, x, y)
        and piece_fits_down(p, x, y)
        and piece_fits_up(p, x, y)
    )


def piece_fits_left(p: Piece, x: int, y: int) -> bool:
    if x <= 0:
        return p.left == 0
    p2 = get_piece(x - 1, y)
    if p2 is None:
        return True
    return p.left == p2.right


def piece_fits_right(p: Piece, x: int, y: int) -> bool:
    if x >= WIDTH - 1:
        return p.right == 0
    p2 = get_piece(x + 1, y)
    if p2 is None:
        return True
    return p.right == p2.left


def piece_fits_up(p: Piece, x: int, y: int) -> bool:
    if y <= 0:
        return p.up == 0
    p2 = get_piece(x, y - 1)
    if p2 is None:
        return True
    return p.up == p2.down


def piece_fits_down(p: Piece, x: int, y: int) -> bool:
    if y >= HEIGHT - 1:
        return p.down == 0
    p2 = get_piece(x, y + 1)
    if p2 is None:
        return True
    return p.down == p2.up


def find_next_candidates():
    best_x = None
    best_y = None
    best_candidates = None

    for y in range(HEIGHT):
        for x in range(WIDTH):
            if get_piece(x, y) is not None:
                continue
            # find unused pieces candidates which fit
            candidates = [p for p in pieces if not p.used and piece_fits(p, x, y)]

            if best_candidates is None or len(candidates) < len(best_candidates):
                best_x = x
                best_y = y
                best_candidates = candidates
                if len(best_candidates) == 1:
                    return best_x, best_y, best_candidates
    return best_x, best_y, best_candidates


solutions = []


def solve_puzzle():
    # we've found a solution if we've used all the pieces
    if all(p.used for p in pieces):
        solutions.append(render_puzzle())
        return

    # otherwise, look for the next candidate location to place a piece
    x, y, candidates = find_next_candidates()

    for p in candidates:
        # mark puzzle location and piece as used
        set_piece(x, y, p)
        p.used = True
        # recursively solve remainder of puzzle
        solve_puzzle()
        # unmark puzzle location and piece
        set_piece(x, y, None)
        p.used = False


def render_puzzle():
    output = ""
    for y in range(HEIGHT):
        for j in range(4):
            for x in range(WIDTH):
                for i in range(4):
                    piece = get_piece(x, y)
                    if piece is None:
                        output += "\033[0;30m?"
                        continue
                    color = piece.colors[j][i]
                    if color == "W":
                        output += "\033[0m "
                    elif color == "R":
                        output += "\033[0;31m#"
                    elif color == "Y":
                        output += "\033[1;33m#"
                    elif color == "B":
                        output += "\033[0;34m#"
                    else:
                        raise ValueError("Invalid color")
            output += "\n"
    output += "\033[0m"
    return output


solve_puzzle()

print(f"FOUND {len(solutions)} SOLUTION")
print()

for solution in solutions:
    print(solution)
