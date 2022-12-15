from collections import namedtuple
Pt = namedtuple("Pt", "x y")

def parse_line(l):
    ws = l.split(" ")
    sx,sy = [int(w[2:-1]) for w in ws[2:4]]
    bx,by = [int(w[2:-1]) for w in ws[8:]]
    return (Pt(sx,sy), Pt(bx,by))

def read(filename):
    f = open(filename)
    s = [parse_line(l) for l in f.readlines()]
    f.close()
    return s

def dist(p1, p2):
    return abs(p1.x-p2.x) + abs(p1.y-p2.y)

"""Returns a dict b where, for any y in b.keys(), b[y] is the pair (xmin, xmax) such that for every xmin <= x <= xmax, (x,y) is within distance d from the point p."""
def ball(p, d):
    assert d > 0
    b = dict()
    for dy in range(-d,d,1):
        dx = d - abs(dy)
        b[p.y + dy] = (p.x - dx, p.x + dx)
    return b

def test_ball():
    p = Pt(2,18)
    d = dist(Pt(2,18),Pt(-2,15))
    b = ball(p,d)
    for y in b.keys():
        xmin, xmax = b[y]
        for x in range(xmin, xmax + 1, 1):
            assert dist(p, Pt(x,y)) <= d
        assert dist(p, Pt(xmin-1,y)) > d
        assert dist(p, Pt(xmax+1,y)) > d

def disjoint(l1,r1,l2,r2):
    #assert l1 <= r1 and l2 <= r2
    if l1 > l2: l1, l2 = l2, l1
    return r1 < l2
    
class Region1D:
    """A Region is represented as a finite set of non-overlapping closed intervals."""
    def __init__(self):
        self.bounds = set()
    
    def find_overlap(self, left, right):
        for lb, rb in self.bounds:
            if not disjoint(lb,rb,left,right):
                return (lb,rb)
        return None
        
    def add(self, left, right):
        """Add the interval [left, right] to the region"""
        ov = self.find_overlap(left, right)
        if ov is None:
            self.bounds.add((left,right))
        else:
            self.bounds.remove(ov)
            self.add(min(ov[0],left),max(ov[1],right))

    def size(self):
        t = 0
        for b in self.bounds:
            t += b[1] - b[0] + 1
        return t

def coverage(y, balls, beacons):
    xcov = Region1D()
    for b in balls:
        if y in b.keys():
            xmin, xmax = b[y]
            xcov.add(xmin,xmax)
    c = len([b for b in set(beacons) if b.y == y])
    print(xcov.bounds)
    return xcov.size() - c



"""Part 2. 
Suppose the beacon is at location (px, py).
If a sensor is at location (sx, sy) and the distance of the closest beacon is d, 
then we must have one of:
x + y > d + sx + sy (p is upper right to s) or
x + y < sx + sy - d (p is lower left to s)  or
x - y > d + sx - sy (p is lower right to s) or
x - y < sx - sy - d (p is upper left to s).

Each of the 20 or so beacons thus excludes that 
(x + y, x - y) is in [sx + sy - d, sx + sy + d] x [sx - sy - d, sx - sy + d].
We are excluding squares out of the (x+y,x-y)-plane.
We also know that 0 <= x, y <= 4_000_000.
"""
from z3 import *

if __name__ == "__main__":
    data = read("input.txt")

    # part 1 (slow)
    # bs = [ball(s, dist(s,b)) for s,b in data]
    # print(coverage(2_000_000, bs, [b for _,b in data]))

    # part 2 (fast, with z3)
    x = Int('x')
    y = Int('y')
    MAX = 4_000_000
    sol = Solver()
    sol.add(0 <= x, x <= MAX, 0 <= y, y <= MAX)
    for s,b in data:
        d = dist(s,b)
        sol.add(Or(x + y > s.x + s.y + d, 
                   x + y < s.x + s.y - d, 
                   x - y > s.x - s.y + d, 
                   x - y < s.x - s.y - d))
    sol.check()
    m = sol.model()
    print(m.eval(x * 4_000_000 + y))
    