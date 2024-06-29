note_mapping = {
    1: "→",
    2: "↘",
    3: "↓",
    4: "↙",
    5: "←",
    6: "↖",
    7: "↑",
    0: "↗",
}


def convert(s: str) -> int:
    return note_mapping[int(s[::-1], 2)]


assert convert("100") == "→"
assert convert("010") == "↘"
assert convert("001") == "↙"
assert convert("000") == "↗"


pattern = """
        011 110 100 110 011 110 100 110 011 001

    010 001 011 001 010 001 000 101 110 101 000 101

110 101 111 101 010 101 111 101 010 101 011 110 100 110

011 110 100 110 011 001 010 001 011 001 010 001 011 000

011 001 000 111 101 110 111 011 001 101 111 011 101 011
"""

for line in pattern.splitlines():
    print(" ".join(convert(s) for s in line.split()))
