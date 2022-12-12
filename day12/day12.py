from math import inf
from typing import Dict, Tuple, Set, Any

ELEV: Dict[str, int] = {chr(x + 96): x for x in range(1,27,1)}
ELEV['S'] = 1
ELEV['E'] = 26

def read(filename):
    with open(filename) as f:
        rawgrid = [[c for c in l.rstrip()] for l in f.readlines()]
    H = len(rawgrid)
    W = len(rawgrid[0])
    grid: Dict[Tuple[int,int],int] = dict()
    s: Tuple[int,int] = (-1,-1)
    e: Tuple[int,int] = (-1,-1)
    for i in range(0,H,1):
        for j in range(0,W,1):
            grid[(i,j)] = ELEV[rawgrid[i][j]]
            if rawgrid[i][j] == "S":
                s = (i,j)
            if rawgrid[i][j] == "E":
                e = (i,j)
    return grid, H, W, s, e

def graph(g: Dict[Tuple[int,int],int], reverse=False):
    edges: Dict[Tuple[int,int],Set[Tuple[int,int]]] = {p : set() for p in P}
    for q in P:
        i,j = q
        for p in [(i-1,j),(i,j-1),(i+1,j),(i,j+1)]:
            if p in g.keys() and g[p] <= g[(i,j)] + 1:
                if reverse: edges[p].add(q)
                else: edges[q].add(p)
    return edges

def shortest_path_to(G: Dict[Tuple[int,int], Set[Tuple[int,int]]], s):
    # d[q] is the length of a shortest path from s to q
    d: Dict[Tuple[int,int],Any] = {p: inf for p in P}    
    # pr[q] is the previously visited node 
    pr: Dict[Tuple[int,int], Tuple[int,int]] = dict()
    
    Q = []
    for p in P:
        Q.append(p)
    d[s] = 0
    Q = sorted(Q, key=lambda p: d[p])

    while len(Q) > 0:
        u = Q.pop(0)
        for v in G[u]:
            if v in Q:
                alt = d[u] + 1
                if alt < d[v]:
                    d[v] = alt
                    pr[v] = u
        Q = sorted(Q, key=lambda p: d[p])
    return d

def gridstr(g) -> str:
    return "\n".join(",".join(str(g[(i,j)]) for j in range(W)) for i in range(H))

if __name__ == "__main__":
    grid, H, W, s, e = read("input.txt")
    P = {(i,j) for i in range(H) for j in range(W)} # all points
    # part 1
    G = graph(grid)
    d = shortest_path_to(G,s)
    print(d[e])
    # part 2
    G2 = graph(grid, reverse=True)
    d2 = shortest_path_to(G2,e)
    print(min(d2[x] for x in P if grid[x] == 1))