import sys

class Cell:
    def __init__(self, prv, nxt, addr, val: int):
        self.prv = prv
        self.nxt = nxt
        self.val = val
    
    def move_right(self):
        a,b,c,d = self.prv, self, self.nxt, self.nxt.nxt
        a.nxt, c.prv, c.nxt, b.prv, b.nxt, d.prv = c, a, b, c, d, b
    
    def move_left(self):
        a,b,c,d = self.prv.prv, self.prv, self, self.nxt
        a.nxt, c.prv, c.nxt, b.prv, b.nxt, d.prv = c, a, b, c, d, b

    def find_value(self, v):
        cur = self
        while cur.val != v:
            cur = cur.nxt
        return cur

class List:
    def __init__(self, z):
        self.zero = z
    
    def __repr__(self):
        s = "["
        cur = self.zero
        while cur.nxt != self.zero:
            s += str(cur.val) + ", "
            cur = cur.nxt
        s += str(cur.val) + "]"
        return s
    
    def find_address(self, i):
        cur = self.zero
        while cur.origaddr != i:
            cur = cur.nxt
            print(cur.origaddr)
        return cur

def read(filename):
    with open(filename) as f:
        xs = [int(l.rstrip()) for l in f.readlines()]
    return xs

def main():
    raw = read(sys.argv[1])
    N = len(raw)
    prevc = Cell(None, None, 0, raw[0])
    cells = [prevc]
    newc = Cell(None, None, -1, -1) 
    zero_loc = -1
    for i in range(1,N):
        newc = Cell(prevc, None, i, raw[i])
        prevc.nxt = newc
        prevc = newc
        cells.append(newc)
        if raw[i] == 0:
            zero_loc = i
    
    cells[-1].nxt = cells[0]
    cells[0].prv = cells[-1]
    l = List(cells[zero_loc])

    #print(l)
    print(N)
    for i in range(N):
        #if i % 500 == 0:
        #    print(i)
        c = cells[i]
        if c.val > 0:
            for _ in range(c.val):
                c.move_right()
        else:
            for _ in range(abs(c.val)):
                c.move_left()
        #print(l)
    
    c = cells[zero_loc]
    v = 0
    for i in range(3):
        for _ in range(1000):
            c = c.nxt
        v += c.val
    print(v)



if __name__ == "__main__":
    main()