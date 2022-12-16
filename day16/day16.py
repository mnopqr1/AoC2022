NAME = dict()
ID = dict()
GREEDY = False

import copy

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


def solve(nodes, values):
    """D[t][n][s] with 2 <= t <= 30, n a node id, and s a set of valuable nodes (represented as 
    bitstrings), contains the maximum attainable value at time t when starting from node n if the 
    nodes in s are still closed."""

    # Initialization, t = 2.
    # All you can do is open the valve where you are now, if it is still closed, and get 1 minute of pressure out of it.
    D = [[], []]
    maxval = [[]] * N
    for n in range(N):
        maxval[n] = [0] * V
        for s in range(V):
            # the valve is still closed
            if n in valuable and (s >> VAL_ID[n]) % 2:
                maxval[n][s] = values[n]
    D.append(maxval)

    # now work back in time
    for t in range(3, 31):
        maxval = [[]] * N
        for n in range(N):
            maxval[n] = [0] * V
            for s in range(V):
                scores = []
                # option 1: open the valve where you are now, if it's valuable & closed
                if n in valuable and (s >> VAL_ID[n]) % 2:
                    thisvalve = values[n] * (t-1)
                    new_s = s - (1 << VAL_ID[n])  # set valve to open
                    scores.append(thisvalve + D[t-1][n][new_s])
                # option 2: go somewhere else
                for m in nodes[n]:  # for each neighbor node
                    scores.append(D[t-1][m][s])
                maxval[n][s] = max(scores)
        D.append(maxval)
    ALL = V - 1
    return D[30][ID["AA"]][ALL]

import numpy as np

def solve2(nodes, valves):
    """At iteration t, if n1 and n2 are node ids,
    then D[n1][n2] is a matrix V -> Int which contains at index s
    the maximum attainable value with t + 2 minutes left if you are in n1, the elephant is in n2, and the set of currently closed valves is s."""
    # print(N * N, V)

    # Initialization, t = 2.
    # All you can do is open the valve where you are now, 
    # if it is still closed, and get 1 minute of pressure out of it.
    
    # has[n] is the array mask of sets containing n
    has = {n: ((np.arange(V) >> VAL_ID[n]) % 2) for n in range(N) if IS_VAL[n]}

    D = np.zeros((N,N,V))
    values = [valves[i] for i in range(N)]

    for n1 in range(N):
        for n2 in range(N):
            if IS_VAL[n1]:
                D[n1][n2] += values[n1] * has[n1] 
                if IS_VAL[n2] and n2 != n1:
                    D[n1][n2] += values[n2] * has[n2]
    # print(D[ID["AA"]][ID["AA"]])
    # now work back in time
    for t in range(3, 27):
        for k in range(len(values)): # values increase with time
            values[k] += valves[k]
        print(t)
        newD = np.zeros((N,N,V), dtype=np.int32)
        for n1 in range(N):
            for n2 in range(N):
                myvalue = values[n1]
                elvalue = values[n2]
                # option 1: both open valve where you are now
                if IS_VAL[n1] and IS_VAL[n2]:
                    if n1 != n2:
                        newD[n1][n2] = myvalue * has[n1] + elvalue * has[n2]
                        new_s = np.arange(V) - (1 << VAL_ID[n1]) * has[n1] - (1 << VAL_ID[n2]) * has[n2]
                        for i in range(V):
                            newD[n1][n2][i] += D[n1][n2][new_s[i]]
                    else:
                        newD[n1][n2] = myvalue * has[n1]
                        new_s = np.arange(V) - (1 << VAL_ID[n1]) * has[n1]
                        for i in range(V):
                            newD[n1][n2][i] += D[n1][n2][new_s[i]]
                # option 2: you go somewhere else, elephant opens valve
                if IS_VAL[n2]:
                    new_s = np.arange(V) - (1 << VAL_ID[n2]) * has[n2]
                    for m in nodes[n1]:
                        for i in range(V):
                            if D[m][n2][new_s[i]] + elvalue > newD[n1][n2][i]:
                                newD[n1][n2] (D[m][n2][new_s] for m in nodes[n1])
     
    #                     scores.append(myvalve + elvalve + D[n1][n2][new_s])
    #                 # option 2: you go somewhere else, elephant opens valve
    #                 if IS_VAL[n2] and (s >> VAL_ID[n2]) % 2:
    #                     elvalve = values[n2] * (t-1)
    #                     new_s = s - (1 << VAL_ID[n2])
    #                     best = max(D[m][n2][new_s] for m in nodes[n1])
    #                     scores.append(elvalve + best)
    #                 # option 3: elephant goes somewhere else, you open valve
    #                 if IS_VAL[n1] and (s >> VAL_ID[n1]) % 2:
    #                     myvalve = values[n1] * (t-1)
    #                     new_s = s - (1 << VAL_ID[n1])
    #                     best = max(D[n1][m][new_s] for m in nodes[n2])
    #                     scores.append(myvalve + best)
    #                 # option 4: you both go somewhere else
    #                 scores.append(max(D[m1][m2][s] for m1 in nodes[n1] for m2 in nodes[n2]))
    #                 maxval[n1][n2][s] = max(scores)
        D = copy.deepcopy(newD)
    ALL = V - 1
    return D[ID["AA"]][ID["AA"]][ALL]

## correct on example but too slow

from functools import lru_cache

def is_in(s, v):
    return (s >> VAL_ID[v]) % 2 == 1

def open_up(s, v):
    assert is_in(s,v)
    return s - (1 << VAL_ID[v])

def compl(s):
    return (V-1) ^ s


@lru_cache(None)
def solve2aux(t, me, el, cl):
    """Best possible value with t minutes left, 
    if I am in position me, the elephant is in position el, 
    and the currently closed valves are cl."""

    if t == 1:
        return PRODUCE[compl(cl)]
    best = 0

    # we both open valves
    if IS_VAL[me] and is_in(cl, me) and IS_VAL[el] and is_in(cl, el):
        newcl = open_up(cl, me)
        if el != me:
            newcl = open_up(newcl, el)
        score = solve2aux(t-1, me, el, newcl)
        if score > best:
            best = score
        # if GREEDY: return score # greedy: open valves if you can RISKY, gives wrong intermediate answers
    # I move, elephant opens valve
    if IS_VAL[el] and is_in(cl, el):
        newcl = open_up(cl, el)
        for newme in NODES[me]:
            score = solve2aux(t-1, newme, el, newcl)
            if score > best:
                best = score
    # elephant moves, I open valve
    if IS_VAL[me] and is_in(cl, me):
        newcl = open_up(cl, me)
        for newel in NODES[el]:
            score = solve2aux(t-1, me, newel, newcl)
            if score > best:
                best = score

    # we both move
    for newme in NODES[me]:
        for newel in NODES[el]:
            score = solve2aux(t-1, newme, newel, cl)
            if score > best:
                best = score
    return best + PRODUCE[compl(cl)]

def solve2rec():
    return solve2aux(26, ID["AA"], ID["AA"], V - 1)

def test_solve2():
    for t in range(2, 27):
        m1 = solve2old(NODES, VALVES, t)
        m2 = solve2aux(t, ID["AA"], ID["AA"], V-1)
        assert m1 == m2, f"first discrepancy: t={t}, old method={m1}, new method={m2}"

def solve2old(nodes, values, tmax):
    """D[n1][n2][s] with 2 <= t <= 30, n1 and n2 node ids, and 
    s a set of valuable nodes (represented as bitstrings), 
    contains the maximum attainable value with t minutes left, 
    if you are in n1, the elephant is in n2, and the 
    valves in s are still closed."""

    # Initialization, t = 2.
    # All you can do is open the valve where you are now, 
    # if it is still closed, and get 1 minute of pressure out of it.
    D = [[]] * N
    for n1 in range(N):
        D[n1] = [[]] * N
        for n2 in range(N):
            D[n1][n2] = [0] * V
            for s in range(V):
                # the valve is still closed, so open it (once)
                if IS_VAL[n1] and is_in(s, n1):
                    D[n1][n2][s] += values[n1]
                if IS_VAL[n2] and is_in(s, n2) and n1 != n2:
                    D[n1][n2][s] += values[n2]

    # now work back in time
    for t in range(3, tmax + 1):
        #print(t)
        maxval = [[]] * N
        for n1 in range(N):
            maxval[n1] = [[]] * N
            for n2 in range(N):
                maxval[n1][n2] = [0] * V
                for s in range(V):
                    scores = []
                    # option 1: you and elephant both open valve where you are now, respectively
                    if IS_VAL[n1] and IS_VAL[n2] and is_in(s, n1) and is_in(s, n2):
                        myvalve = values[n1] * (t-1)
                        # NB if we do this when we are at the same valve we don't get double the pressure!
                        if n1 == n2:
                            elvalve = 0
                            new_s = s - (1 << VAL_ID[n1])
                        else:
                            elvalve = values[n2] * (t-1)
                            new_s = s - (1 << VAL_ID[n1]) - (1 << VAL_ID[n2]) 
                        scores.append(myvalve + elvalve + D[n1][n2][new_s])
                    # option 2: you go somewhere else, elephant opens valve
                    if IS_VAL[n2] and (s >> VAL_ID[n2]) % 2:
                        elvalve = values[n2] * (t-1)
                        new_s = s - (1 << VAL_ID[n2])
                        best = max(D[m][n2][new_s] for m in nodes[n1])
                        scores.append(elvalve + best)
                    # option 3: elephant goes somewhere else, you open valve
                    if IS_VAL[n1] and (s >> VAL_ID[n1]) % 2:
                        myvalve = values[n1] * (t-1)
                        new_s = s - (1 << VAL_ID[n1])
                        best = max(D[n1][m][new_s] for m in nodes[n2])
                        scores.append(myvalve + best)
                    # option 4: you both go somewhere else
                    scores.append(max(D[m1][m2][s] for m1 in nodes[n1] for m2 in nodes[n2]))
                    maxval[n1][n2][s] = max(scores)
        D = copy.deepcopy(maxval)
    ALL = V - 1
    return D[ID["AA"]][ID["AA"]][ALL]


if __name__ == "__main__":
    NODES: list[list[int]]
    NODES, VALVES = read("example.txt")
    N = len(NODES)
    valuable = [n for n in range(N) if VALVES[n] != 0]
    IS_VAL = [n in valuable for n in range(N)]
    V = 2 ** len(valuable)
    VAL_ID = {valuable[i]: i for i in range(len(valuable))}
    T = 0

    PRODUCE = [0] * V
    for s in range(V):
        PRODUCE[s] = sum(VALVES[v] for v in range(N) if IS_VAL[v] and is_in(s,v))
    # print(PRODUCE[0])
    # print(PRODUCE[V-1])
    #print(solve2old(NODES,VALVES,26))
    print(solve2rec())
    # test_solve2()
