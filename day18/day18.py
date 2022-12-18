import sys
import bisect

def read(filename):
    with open(filename) as f:
        pts = [[int(c) for c in l.rstrip().split(",")] for l in f.readlines()]
    return pts

def code(p):
    x,y,z = p
    return x + D * y + D * D * z

def pt(c):
    z = c // (D * D)
    y = (c % (D * D)) // D
    x = (c % (D * D)) % D
    return [x, y, z]

def test_ptcode(pts):
    for p in pts:
        assert pt(code(p)) == p, f"p = {p}, code(p) = {code(p)}, pt(code(p)) = {pt(code(p))}"
    for c in range(D * D * D):
        assert code(pt(c)) == c

def codelist(pts):
    l = []
    for p in pts:
        bisect.insort(l, code(p))
    return l

def is_in(l, pt):
    i = bisect.bisect_left(l, code(pt))
    return i != len(l) and l[i] == code(pt)

def nneighbors(pt, l):
    c = 0
    for axis in [0,1,2]:
        for d in [-1,1]:
            other = [p for p in pt]
            other[axis] += d
            if is_in(l, other): c += 1
    return c

if __name__ == "__main__":
    pts = read(sys.argv[1])
    D = max(max(p) for p in pts) + 1 # dimension
    l = codelist(pts)
    t = 0
    for i in range(len(l)):
        t += 6 - nneighbors(pt(l[i]),l)
    print(t)
    #test_ptcode(pts)
    #print(l[:5])
    #print(min(min(p) for p in pts))