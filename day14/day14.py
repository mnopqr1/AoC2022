from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from math import inf
from typing import Set, Dict, Tuple
MAXINT = 10000
MININT = -10000

@dataclass
class Pt:
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x},{self.y})"

def str_to_pt(s: str):
    x,y = map(int,s.split(","))
    return Pt(x,y)

Material = Enum("Material", "Wall Empty Sand")
WALL = Material.Wall
EMPTY = Material.Empty
SAND = Material.Sand

class Grid:
    def __init__(self):
        self.minx, self.miny, self.maxx, self.maxy = MAXINT, MAXINT, MININT, MININT
        self.g: Dict[Tuple[int,int],Material] = defaultdict(lambda: EMPTY)

    def add_pt(self, p: Pt):
        if p.x < self.minx: self.minx = p.x
        if p.x > self.maxx: self.maxx = p.x
        if p.y < self.miny: self.miny = p.y
        if p.y > self.maxy: self.maxy = p.y
        self.g[(p.x,p.y)] = WALL

    def add_line(self, fix: int, varfr: int, varto: int, vertical: bool):
        if varfr > varto: varfr, varto = varto, varfr
        assert varfr < varto
        curr = varfr
        while curr <= varto:
            P = Pt(fix, curr) if vertical else Pt(curr, fix)
            #print(f"add {P}")
            self.add_pt(P)
            curr += 1
    
    def draw(self,p1,p2):
        P1, P2 = str_to_pt(p1), str_to_pt(p2)
        assert P1.x == P2.x or P1.y == P2.y
        if P1.x == P2.x: #vertical
            self.add_line(P1.x, P1.y, P2.y, True)
        else: #horizontal
            self.add_line(P1.y, P1.x, P2.x, False)

    def possible(self, x, y) -> bool:
        return self.g[(x,y)] == EMPTY
    
    def out_of_bounds(self,x,y) -> bool:
        return y >= self.maxy
    
    def dropsand(self) -> bool: # return True when sand went off grid
        sx, sy = 500, 0
        while True:
            poss = [p for p in [(sx,sy+1), (sx-1,sy+1), (sx+1,sy+1)] if self.possible(*p)]
            if len(poss) == 0: break
            sx, sy = poss[0]
            if self.out_of_bounds(sx,sy): break
        if not self.out_of_bounds(sx,sy): self.g[(sx,sy)] = SAND
        return self.out_of_bounds(sx,sy)

    def __repr__(self) -> str:
        
        s = ""
        for y in range(0, self.maxy+2, 1):
            s += "{:3.0f}".format(y)
            for x in range(self.minx-1, self.maxx+2, 1):
                if self.g[(x,y)] == WALL: s += "#"
                if self.g[(x,y)] == SAND: s += "o"
                if self.g[(x,y)] == EMPTY: s += "."
            s += "\n"
        s += f"Grid lower bound ({self.minx},{self.maxy}) to ({self.maxx}, {self.maxy})\n\n"
        return s

def read(filename):
    G = Grid()
    with open(filename) as f:
        for l in f.readlines():
            lines = l.rstrip().split("->")
            for i in range(len(lines)-1):
                G.draw(lines[i],lines[i+1])
    return G

if __name__ == "__main__":
    G = read("example.txt")
    
    print(G)
    #part 1
    c = 0
    done = False
    while not done:
        done = G.dropsand()
        c += 1
        #print(G)
        #input()
    print(G)
    print(c-1)
