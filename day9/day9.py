DISPLAY = False
# DIMS = (26, 21)

DELTA = {'R': (1,0), 'U': (0,1), 'L': (-1, 0), 'D': (0, -1)}

# found with trial and error for nice displaying
INIT = (70, 180)
# INIT = (11, 5)

LENGTH = 10
INPUTFILE = "input.txt"

"""Input parsing"""
def parse(filename):
    with open(filename) as f:
        lines = [l.split(" ") for l in f.readlines()]
        return [(x, int(y)) for [x,y] in lines]


"""Display functions for debugging"""
def show_grid(w, h, p):
    s = ""
    for y in range(h-1,-1,-1):
        for x in range(0, w, 1):
            found = False
            i = 0
            while i < LENGTH and not found:
                if p[i] == (x,y):
                    s += "H" if i == 0 else str(i)
                    found = True
                i += 1
            if not found: s += "."
        s += "\n"
    print(s)


def show_bool_grid(w,h,v):
    s = ""
    for y in range(h-1,-1,-1):
        for x in range(0, w, 1):
            if v[(x,y)]: s += "#"
            else: s += "."
        s += "\n"
    print(s)


def show_last_grid(p,dims):
    show_grid(dims[0],dims[1],[p[k][-1] for k in range(LENGTH)])


"""Utility functions"""
def touches(t,h):
    return t[0] in [h[0]-1,h[0],h[0]+1] and t[1] in [h[1]-1,h[1],h[1]+1]


def sign(x):
    if x == 0: return 0
    return x / abs(x)


"""Move functions"""
def move_head(h, d):
    return (h[0] + d[0], h[1] + d[1])


def move_tail(h, t):
    hx, hy, tx, ty = h[0], h[1], t[0], t[1]
    assert hx >= 0 and hy >= 0
    if touches(t, h):
        return t
    else:
        tnew = tx + sign(hx - tx), ty + sign(hy - ty)
        assert touches(tnew, h), f"don't touch: t={tnew}, h={h}"
        return tnew


"""Main loop"""
def main(instructions):
    piece = {i: [INIT] for i in range(LENGTH)}

    if DISPLAY: 
        print("== Initial State ==")
        show_last_grid(piece, DIMS)
    
    steps = 0
    for (dir, n) in instructions:
        if DISPLAY: print(f"== {dir} {n} ==")
        d = DELTA[dir]
        steps += n
        for i in range(n):
            d = DELTA[dir]
            piece[0].append(move_head(piece[0][-1], d))
            for p in range(1,LENGTH):
                head = piece[p-1][-1] # the body part ahead of this one
                tail = piece[p][-1] # current position of this body part
                piece[p].append(move_tail(head, tail))
        if DISPLAY: show_last_grid(piece, DIMS)

    assert all(len(piece[i]) == len(piece[0]) for i in range(LENGTH))

    width = max(pos[0] for pos in piece[0]) + 1
    height = max(pos[1] for pos in piece[0]) + 1
    tvisits = {(x,y) : False for x in range(width) for y in range(height)}
    for i in range(steps+1):
        tvisits[piece[LENGTH-1][i]] = True

    if DISPLAY: show_bool_grid(width, height, tvisits)
    print(sum(tvisits[(x,y)] for x in range(width) for y in range(height)))


if __name__ == "__main__":
    instructions = parse(INPUTFILE)
    main(instructions)
