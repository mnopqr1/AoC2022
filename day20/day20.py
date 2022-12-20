import sys


class Cell:
    def __init__(self, prv, nxt, val: int):
        self.prv = prv
        self.nxt = nxt
        self.val = val

    def move_right(self):
        a, b, c, d = self.prv, self, self.nxt, self.nxt.nxt
        a.nxt, c.prv, c.nxt, b.prv, b.nxt, d.prv = c, a, b, c, d, b


def read(filename):
    with open(filename) as f:
        xs = [int(l.rstrip()) for l in f.readlines()]
    return xs


def initialize(raw):
    N = len(raw)
    prevc = Cell(None, None, raw[0])
    cells = [prevc]
    newc = Cell(None, None, -1)
    zero_loc = -1
    for i in range(1, N):
        newc = Cell(prevc, None, raw[i])
        prevc.nxt = newc
        prevc = newc
        cells.append(newc)
        if raw[i] == 0:
            zero_loc = i
    cells[-1].nxt = cells[0]
    cells[0].prv = cells[-1]
    return cells, zero_loc


def main(key, reps):
    raw = read(sys.argv[1])
    cells, zero_loc = initialize(raw)
    N = len(cells)

    for _ in range(reps):
        for i in range(N):
            c = cells[i]
            shift = (c.val * key) % (N - 1)
            for _ in range(shift):
                c.move_right()

    c = cells[zero_loc]
    v = 0
    for i in range(3):
        for _ in range(1000):
            c = c.nxt
        v += c.val * key
    print(v)


if __name__ == "__main__":
    # part 1
    main(1, 1)

    # part 2
    main(811589153, 10)
