from itertools import product
from math import lcm
import sys


def read(filename) -> list[str]:
    with open(filename) as f:
        lines = [l.rstrip() for l in f.readlines()]
    h, w = len(lines), len(lines[0])

    # check input assumptions
    assert lines[0][1] == "." and all(lines[0][j] == "#" for j in range(2,w))
    assert lines[h-1][w-2] == "." and all(lines[h-1][j] == "#" for j in range(0,w-2))
    assert all(lines[i][0] == "#" and lines[i][w-1] == "#" for i in range(0,h))

    # forget padding
    real = [l[1:-1] for l in lines[1:-1]]
    return real

def parse(board) -> tuple[list[set[tuple[int,int]]], int, int, int]:
    h, w = len(board), len(board[0])
    p = lcm(h,w)
    #obs = [dict() for _ in range(p)]
    free = [set() for _ in range(p)]
    # for x, y in product(range(w), range(h)):
    #     for i in range(p):
    #         # obs[i][(y,x)] = int(board[y][(x-i)%w] == ">") + \
    #         #                 int(board[y][(x+i)%w] == "<") + \
    #         #                 int(board[(y-i)%h][x] == "v") + \
    #         #                 int(board[(y+i)%h][x] == "^")
    #         occupied = board[y][(x-i)%w] == ">" or board[y][(x+i)%w] == "<" or board[(y-i)%h][x] == "v" or board[(y+i)%h][x] == "^"
    #         #obs[i][(y,x)] = occupied
    
    for i in range(p):
        free[i] = {(y,x) 
             for y,x in product(range(h),range(w)) 
             if not (board[y][(x-i)%w] == ">" or board[y][(x+i)%w] == "<" or board[(y-i)%h][x] == "v" or board[(y+i)%h][x] == "^")}

    return free, h, w, p

SYMBOL: dict[bool, str] = {True: "#", False: "."}
def to_str(free: set[tuple[int,int]], h: int, w: int) -> str:
    return "\n".join("".join(SYMBOL[(y,x) not in free] for x in range(w)) for y in range(h))


if __name__ == "__main__":

    board = read(sys.argv[1])
    free, h, w, p = parse(board)
    print(f"Period: {p}, Board height: {h}, width: {w}")
    tmin = min(t for t in range(1,p) if (0,0) in free[t])
    print(f"First time > 0 that there is no blizzard at (0,0): {tmin}")
    for t in range(tmin, tmin+1):
        print(f"Board at t={t}")
        print(to_str(free[t], h, w))
