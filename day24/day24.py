from itertools import product
from math import lcm
import sys

STEPS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
SYMBOL: dict[bool, str] = {True: "#", False: "."}
debug = False

def to_str(free: set[tuple[int, int]], h: int, w: int) -> str:
    return "\n".join("".join(SYMBOL[(y, x) not in free] for x in range(w)) for y in range(h))


def read(filename) -> list[str]:
    with open(filename) as f:
        lines = [l.rstrip() for l in f.readlines()]

    # forget padding
    real = [l[1:-1] for l in lines[1:-1]]
    return real


def parse(board) -> tuple[list[set[tuple[int, int]]], int, int, int]:
    h, w = len(board), len(board[0])
    p = lcm(h, w)
    free = [set() for _ in range(p)]
    for i in range(p):
        free[i] = {(y, x)
                   for y, x in product(range(h), range(w))
                   if not (board[y][(x-i) % w] == ">" or board[y][(x+i) % w] == "<" or board[(y-i) % h][x] == "v" or board[(y+i) % h][x] == "^")}

    return free, h, w, p


def first_time(tmin, s, e):
    P = len(FREE)
    last = {s}
    done = False
    t = tmin
    while not done:
        new = set()
        t = t + 1
        for (px, py) in last:
            nextposs = set((px+dx, py+dy)
                           for (dx, dy) in STEPS if (px+dx, py+dy) in FREE[t % P])
            if e in nextposs:
                done = True
                break
            new.update(nextposs)
        last = new
        # print(t, len(last))
    return t + 1


if __name__ == "__main__":
    board = read(sys.argv[1])
    FREE, h, w, p = parse(board)
    if debug: print(f"Period: {p}, Board height: {h}, width: {w}")
    tmin = min(t for t in range(1, p) if (0, 0) in FREE[t])
    if debug: print(f"First time > 0 that there is no blizzard at (0,0): {tmin}")
    START = (0, 0)
    END = (h-1, w-1)
    t = first_time(tmin, START, END)
    print(t)
