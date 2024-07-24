from dataclasses import dataclass

data = """
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

items = data.split()

while items:
    code = items[0]
    up = int(code[0])
    right = int(code[1])
    down = int(code[2])
    left = int(code[3])
    colors = [list(c) for c in items[1:5]]
    pieces.append(Piece(up, right, down, left, colors, False))
    items = items[5:]


# helper func to do include range without writing + 1 everywhere
def rangeinc(a, b):
    return range(a, b + 1)


LEFT = 0
RIGHT = 9
TOP = 0
BOTTOM = 4


puzzle = [[None for _ in rangeinc(LEFT, RIGHT)] for _ in rangeinc(TOP, BOTTOM)]


def piece_fits(p: Piece, x: int, y: int):
    return (
        piece_fits_left(p, x, y)
        and piece_fits_right(p, x, y)
        and piece_fits_down(p, x, y)
        and piece_fits_up(p, x, y)
    )


def piece_fits_left(p: Piece, x: int, y: int) -> bool:
    if x <= LEFT:
        return p.left == 0
    p2 = puzzle[y][x - 1]
    if p2 is None:
        return True
    return p.left == p2.right


def piece_fits_right(p: Piece, x: int, y: int) -> bool:
    if x >= RIGHT:
        return p.right == 0
    p2 = puzzle[y][x + 1]
    if p2 is None:
        return True
    return p.right == p2.left


def piece_fits_up(p: Piece, x: int, y: int) -> bool:
    if y <= TOP:
        return p.up == 0
    p2 = puzzle[y - 1][x]
    if p2 is None:
        return True
    return p.up == p2.down


def piece_fits_down(p: Piece, x: int, y: int) -> bool:
    if y >= BOTTOM:
        return p.down == 0
    p2 = puzzle[y + 1][x]
    if p2 is None:
        return True
    return p.down == p2.up


def find_next_candidates():
    best_x = None
    best_y = None
    best_candidates = None

    for y in rangeinc(TOP, BOTTOM):
        for x in rangeinc(LEFT, RIGHT):
            if puzzle[y][x] is not None:
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


def solve_puzzle():
    x, y, candidates = find_next_candidates()

    # if there are no more candidates then stop
    if candidates is None:
        render_puzzle()
        return True

    for p in candidates:
        # mark puzzle location and piece as used
        puzzle[y][x] = p
        p.used = True
        render_puzzle()
        if solve_puzzle():
            return True
        # unmark puzzle location and piece
        puzzle[y][x] = None
        p.used = False
    return False


def render_puzzle():
    output = "\033c\033[0m"

    for y in rangeinc(TOP, BOTTOM):
        for j in range(4):
            for x in rangeinc(LEFT, RIGHT):
                for i in range(4):
                    piece = puzzle[y][x]
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
    print(output)


solve_puzzle()
