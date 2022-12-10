with open("input.txt") as f:
    g = [[int(c) for c in line.rstrip()] for line in f.readlines()]

h, w = len(g), len(g[0])
vis = {(i,j) : False for i in range(h) for j in range(w)}

for i, l in enumerate(g):
    m = g[i][0]
    vis[(i,0)] = True
    for j in range(1,w):    
        if l[j] > m:
            vis[(i,j)] = True
            m = l[j]
    
    m = g[i][w-1]
    vis[(i,w-1)] = True
    for j in range(w-2,0,-1):
        if l[j] > m:
            vis[(i,j)] = True
            m = l[j]

for j in range(w):
    m = g[0][j]
    vis[(0,j)] = True
    for i in range(1, h):
        if g[i][j] > m:
            vis[(i,j)] = True
            m = g[i][j]
    
    vis[(h-1,j)] = True
    m = g[h-1][j]
    i = h-2
    for i in range(h-2, 0, -1):
        if g[i][j] > m:
            vis[(i,j)] = True
            m = g[i][j]
        

# from pprint import pprint
# pprint([[vis[(i,j)] for j in range(w)] for i in range(h)])
print(sum(vis[(i,j)] for i in range(h) for j in range(w)))
