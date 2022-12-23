from collections import defaultdict
import sys, os
from time import sleep

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

display = True

def read(filename) -> dict[int, set[int]]:
    with open(filename) as f:
        lines = [l.rstrip() for l in f.readlines()]
    board = defaultdict(lambda: set())
    for r, l in enumerate(lines):
        board[r] = {c for c in range(len(l)) if l[c] == "#"}
    return board


def locations(board: dict[int, set[int]]) -> list[tuple[int, int]]:
    res = []
    for r in board.keys():
        for c in board[r]:
            res.append((r, c))
    return res


def size(pts: list[tuple[int, int]]) -> int:
    xmin, xmax = min(pt[0] for pt in pts), max(pt[0] for pt in pts)
    ymin, ymax = min(pt[1] for pt in pts), max(pt[1] for pt in pts)
    return (ymax + 1 - ymin) * (xmax + 1 - xmin)


def is_empty(board: dict[int, set[int]], pt: tuple[int, int], d: tuple[int, int]):
    dx, dy = d
    px, py = pt
    if dy == 0:
        return not (py-1 in board[px + dx] or py in board[px + dx] or py + 1 in board[px+dx])
    if dx == 0:
        return not (py + dy in board[px-1] or py + dy in board[px] or py + dy in board[px+1])


def round(board: dict[int, set[int]], elves: list[tuple[int, int]], n: int):
    done = True
    # request[(x,y)] contains the list of elves who have requested to go to this position
    request: dict[tuple[int, int], list[int]] = defaultdict(lambda: [])
    # propose
    for k, e in enumerate(elves):
        empty_dirs = [DIRS[i % 4]
                      for i in range(n, n+4) if is_empty(board, e, DIRS[i % 4])]
        if len(empty_dirs) in [0, 4]:
            continue
        dx, dy = empty_dirs[0]
        ex, ey = e
        request[(ex + dx, ey + dy)].append(k)

    # move
    for p in request.keys():
        if len(request[p]) == 1:
            k = request[p][0]
            ex, ey = elves[k]
            elves[k] = p
            board[ex].remove(ey)
            assert p[1] not in board[p[0]]
            board[p[0]].add(p[1])
            done = False

    return board, elves, done


def to_str(pts: list[tuple[int, int]]):
    str = ""
    xmin, xmax = min(pt[0] for pt in pts), max(pt[0] for pt in pts)
    ymin, ymax = min(pt[1] for pt in pts), max(pt[1] for pt in pts)
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            if (x, y) in pts:
                str += "🧝"
            else:
                str += " "
        str += "\n"
    return str


if __name__ == "__main__":
    board = read(sys.argv[1])
    elves = locations(board)

    # part 1
    # N = 10
    # for n in range(N):
    #     board, elves, _ = round(board, elves, n)
    #     print(f"==Round {n}==")
    # print(size(elves) - len(elves))

    # part 2
    done = False
    n = 0
    while not done:
        board, elves, done = round(board, elves, n)
        n += 1
        board_str = to_str(elves)
        if display:
            sleep(0.1)
            os.system("clear")
            print(f"==Round {n}==")
            print(board_str)
    print(n)
