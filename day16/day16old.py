NAME = dict()
ID = dict()

from functools import lru_cache
import copy
import time

def read(filename):
    with open(filename) as f:
        lines = [l for l in f.readlines()]
    nodes, values = [[]] * len(lines), [0] * len(lines)
    cnt = 0
    for l in lines:
        ws = l.split(" ")
        currname = ws[1]
        value = int(ws[4][5:-1])
        accnames = [n[:-1] for n in ws[9:]]
        for n in [currname] + accnames:
            if n not in ID.keys():
                ID[n] = cnt
                NAME[cnt] = n
                cnt += 1
        values[ID[currname]] = value
        nodes[ID[currname]] = [ID[n] for n in accnames]
    assert cnt == len(lines) and all(NAME[ID[n]] == n for n in ID.keys())
    return nodes, values


## correct on example but too slow

def is_in(s, v):
    return (s >> VAL_ID[v]) % 2 == 1

def open_up(s, v):
    #assert is_in(s,v)
    return s - (1 << VAL_ID[v])

def add(s, v):
    if is_in(s,v):
        return s
    else:
        return s + (1 << VAL_ID[v])
def compl(s):
    return (VS-1) ^ s

@lru_cache(None)
def solve2aux(t, me, el, op) -> int:
    """Best possible value with t minutes left, 
    if I am in position me, the elephant is in position el, 
    and the currently open valves are op (a bitstring)."""  
    if t <= 0:
        return 0
    if t == 1:
        return PRODUCE[op]

    best = 0
    if IS_VAL[me] and IS_VAL[el]:
        newop = add(add(op, me), el)
        score = solve2aux(t-1, me, el, newop)
        if score > best:
            best = score
    
    elif IS_VAL[me]:
        newop = add(op, me)
        for newelv in VALUABLE:
            tr = SP[el][newelv] # travel time
            score = solve2aux(t-tr, me, newelv, newop) + (tr - 1) * PRODUCE[newop]
            if score > best:
                best = score

    elif IS_VAL[el]:
        newop = add(op, el)
        for newmev in VALUABLE:
            if not is_in(op, newmev):
                tr = SP[me][newmev] # travel time
                score = solve2aux(t-tr, newmev, el, newop) + (tr - 1) * PRODUCE[newop]
                if score > best:
                    best = score
    
    else:
        # assert False # I never call this function in non-valuable nodes
        score = max(solve2aux(t-1, newme, newel, op) for newme in NODES[me] for newel in NODES[el])

    return best + PRODUCE[op]

def solve2rec(t):
    return solve2aux(t, ID["AA"], ID["AA"], 0)

MAXINT = 100000
def roadmap():
    dist = [[]] * N
    for i in range(N):
        dist[i] = [MAXINT] * N
        for j in NODES[i]:
            dist[i][j] = 1
        dist[i][i] = 0
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist
    # only care about valuable valves
    # valdist = [[]] * V
    # for v in range(V):
    #     valdist[v] = [0] * V
    #     for w in range(V):
    #         valdist[v][w] = dist[VALUABLE[v]][VALUABLE[w]]
    # return valdist




if __name__ == "__main__":
    NODES: list[list[int]]
    NODES, VALVES = read("example.txt")
    N = len(NODES)
    VALUABLE = [n for n in range(N) if VALVES[n] != 0]
    IS_VAL = [n in VALUABLE for n in range(N)]
    V = len(VALUABLE)
    VS = 2 ** V
    VAL_ID = {VALUABLE[i]: i for i in range(V)}

    # at coordinate s, the value per minute produced if the valves in s are open
    PRODUCE = [0] * VS
    for s in range(VS):
        PRODUCE[s] = sum(VALVES[v] for v in range(N) if IS_VAL[v] and is_in(s,v))

    # I precompute a roadmap, which at index i, j contains the number of minutes it takes to go from node i to node j
    SP = roadmap()
    # print(SP)
    print(solve2rec(26))
    # t0 = time.time()
    # for t in range(2,27):
    #     #answer = solve2rec(t)
    #     #answer = solve2old(NODES,VALVES,t)
    #     answer = 0
    #     t1 = time.time()
    #     print(f"t={t}, answer={answer}, took {t1-t0} seconds")
    #     t0 = t1
