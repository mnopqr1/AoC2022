from itertools import product
from math import lcm
import sys

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

STEPS = {"start": [(0, 0), (1, 0)], "end": [(0, 0), (-1, 0)],
         "other": [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]}

def first_time(tmin, s, e):
    P = len(FREE)
    last = {s}
    done = False
    t = tmin
    while not done:
        new = set()
        for (px, py) in last:
            if (px, py) == START: k = "start"
            if (px, py) == END:   k = "end"
            else:                 k = "other"
            nextposs = set((px+dx, py+dy)
                           for (dx, dy) in STEPS[k] if (px+dx, py+dy) in FREE[t % P])
            if e in nextposs:
                done = True
                break
            new.update(nextposs)
        last = new
        t = t + 1
    return t-1


if __name__ == "__main__":
    board = read(sys.argv[1])
    FREE, H, W, P = parse(board)
    START = (-1, 0)
    END = (H, W-1)
    for p in range(P):
        FREE[p].update({START, END})

    t = first_time(1, START, END)
    t = first_time(t, END, START)
    t = first_time(t, START, END)
    print(t)
