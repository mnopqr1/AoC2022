with open("input.txt") as f:
    lines = [l.split(" ") for l in f.readlines()]
    instructions = [(x, int(y)) for [x,y] in lines]

DELTA = {'R': (1,0), 'U': (0,1), 'L': (-1, 0), 'D': (0, -1)}

def touches(t,h):
    return t[0] in [h[0]-1,h[0],h[0]+1] and t[1] in [h[1]-1,h[1],h[1]+1]

def same_row(t,h):
    return t[1] == h[1]
def same_col(t,h):
    return t[0] == h[0]

def move(h,t,d):
    hx, hy, tx, ty, dx, dy = h[0], h[1], t[0], t[1], d[0], d[1]
    hnew = (hx + dx, hy + dy)
    assert hx >= 0 and hy >= 0
    if touches(t, hnew):
        tnew = t
    elif same_row(t, hnew) or same_col(t, hnew):
        tnew = (tx + dx, ty + dy)
    else: # diagonal move case
        if d[0] == 0: # h's move was vertical
            tnew = (hnew[0], ty + dy) # then t aligns vertically with h
        else: # h's move was horizontal
            tnew = (tx + dx, hnew[1]) # then t aligns horizontally with h
    assert touches(tnew, hnew), f"don't touch: t={tnew}, h={hnew}"
    return hnew, tnew

def show_grid(w, h, H, T):
    s = ""
    for y in range(h-1,-1,-1):
        for x in range(0, w, 1):
            if H == (x,y):
                if T == (x,y): s += "X"
                else: s += "H"
            elif T == (x,y): s += "T"
            else: s += "."
        s += "\n"
    print(s)

h = [(1000,1000)]
t = [(1000,1000)]
for (dir, n) in instructions:
    for i in range(n):
        newh, newt = move(h[-1],t[-1],DELTA[dir])
        h.append(newh)
        t.append(newt)
assert len(h) == len(t)
width = max(hpos[0] for hpos in h) + 1
height = max(hpos[1] for hpos in h) + 1
Tvisits = {(x,y) : False for x in range(width) for y in range(height)}
for i in range(len(h)):
    #show_grid(width, height, h[i], t[i])
    Tvisits[t[i]] = True
print(sum(Tvisits[(x,y)] for x in range(width) for y in range(height)))
