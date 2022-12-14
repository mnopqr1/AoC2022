from collections import defaultdict, namedtuple
from enum import Enum
from typing import Dict, Tuple
SANTAMODE = True
MAXINT = 10000
MININT = -10000
Pt = namedtuple("Pt", "x y")


def str_to_pt(s: str):
    x, y = map(int, s.split(","))
    return Pt(x, y)


Material = Enum("Material", "Wall Empty Sand")
WALL = Material.Wall
EMPTY = Material.Empty
SAND = Material.Sand
if SANTAMODE:
    SYMBOL = {WALL: "🎅", EMPTY: "  ", SAND: "🎄"}
else:
    SYMBOL = {WALL: "#", EMPTY: ".", SAND: "o"}


class Grid:
    def __init__(self):
        self.minx, self.maxx, self.maxy = MAXINT, MININT, MININT
        self.g: Dict[Tuple[int, int], Material] = defaultdict(lambda: EMPTY)

    def add_wall(self, p: Pt):
        if p.x < self.minx:
            self.minx = p.x
        if p.x > self.maxx:
            self.maxx = p.x
        if p.y > self.maxy:
            self.maxy = p.y
        self.g[(p.x, p.y)] = WALL

    def add_line(self, fix: int, varfr: int, varto: int, vertical: bool):
        if varfr > varto:
            varfr, varto = varto, varfr
        curr = varfr
        while curr <= varto:
            P = Pt(fix, curr) if vertical else Pt(curr, fix)
            self.add_wall(P)
            curr += 1

    def draw(self, p1, p2):
        P1, P2 = str_to_pt(p1), str_to_pt(p2)
        if P1.x == P2.x:  # vertical
            self.add_line(P1.x, P1.y, P2.y, True)
        else:             # horizontal
            self.add_line(P1.y, P1.x, P2.x, False)

    def possible(self, x, y) -> bool:
        return self.g[(x, y)] == EMPTY and y <= self.maxy + 1

    def dropsand(self) -> bool:  # return True when this was last piece
        sx, sy = 500, 0
        while True:
            poss = [p for p in [(sx, sy+1), (sx-1, sy+1),
                                (sx+1, sy+1)] if self.possible(*p)]
            if len(poss) == 0:
                break
            sx, sy = poss[0]
        self.g[(sx, sy)] = SAND
        return (sx, sy) == (500, 0)

    def __repr__(self) -> str:
        s = ""
        for y in range(0, self.maxy+3, 1):
            s += "{:3.0f}".format(y) + " "
            for x in range(self.minx-100, self.maxx+100, 1):
                s += SYMBOL[self.g[(x, y)]]
            s += "\n"
        return s


def read(filename):
    G = Grid()
    with open(filename) as f:
        for l in f.readlines():
            lines = l.rstrip().split("->")
            for i in range(len(lines)-1):
                G.draw(lines[i], lines[i+1])
    return G


if __name__ == "__main__":
    G = read("input.txt")

    print(G)
    c = 0
    done = False
    while not done:
        done = G.dropsand()
        c += 1
    print(G)
    print(c)
