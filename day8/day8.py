with open("example.txt") as f:
    grid = [[int(x) for x in xs.rstrip()] for xs in f.readlines()]

def get_col(grid, j):
    return [line[j] for line in grid]

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3
DIRS = [LEFT, UP, RIGHT, DOWN]
DIRNAME = {LEFT: "left", UP: "up", RIGHT: "right", DOWN: "down"}

h, w = len(grid), len(grid[0])

# v[(i,j,d)] will contain the number of trees seen from (i,j) looking in dir d before being blocked
v = {(i,j,d) : -1 for i in range(h) for j in range(w) for d in DIRS}

for i, line in enumerate(grid):
    for j in range(w):
        n = 0
        while j - n > 0 and line[j-n-1] < line[j]:
            n = n + 1
        if j - n > 0: n = n + 1
        v[(i,j,LEFT)] = n

        n = 0
        while j + n < w - 1 and line[j+n+1] < line[j]:
            n = n + 1
        if j + n < w - 1: n = n + 1
        v[(i,j,RIGHT)] = n

for j in range(w):
    col = get_col(grid, j)
    for i in range(h):
        n = 0
        while i + n < h - 1 and col[i+n+1] < col[i]:
            n = n + 1
        if i + n < h - 1: n = n + 1
        v[(i,j,DOWN)] = n

        n = 0
        while i - n > 0 and col[i-n-1] < col[i]:
            n = n + 1
        if i - n > 0: n = n + 1
        v[(i,j,UP)] = n

# from pprint import pprint
# for d in DIRS:
#     print(DIRNAME[d])
#     pprint([[v[(i,j,d)] for j in range(w)] for i in range(h)])

s = max(v[(i,j,DOWN)] * v[(i,j,LEFT)] * v[(i,j,UP)] * v[(i,j,RIGHT)] for i in range(h) for j in range(w))
print(s)