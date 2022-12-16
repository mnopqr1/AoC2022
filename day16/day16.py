NAME = dict()
ID = dict()

import copy

def read(filename):
    with open(filename) as f:
        lines = [l for l in f.readlines()]
    nodes, values = [0] * len(lines), [0] * len(lines)
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


def solve2(nodes, values):
    """At iteration t, D[n1][n2][s] with n1 and n2 node ids, and 
    s a set of valuable nodes (represented as bitstrings), 
    contains the maximum attainable value with t + 2 minutes left, 
    if you are in n1, the elephant is in n2, and the 
    valves in s are still closed."""

    # Initialization, t = 2.
    # All you can do is open the valve where you are now, 
    # if it is still closed, and get 1 minute of pressure out of it.
    D = [[]] * N
    print(N * N, V)
    for n1 in range(N):
        D[n1] = [[]] * N
        for n2 in range(N):
            D[n1][n2] = [0] * V
            for s in range(V):
                # the valve is still closed, so open it (once)
                if IS_VAL[n1] and (s >> VAL_ID[n1]) % 2:
                    D[n1][n2][s] += values[n1]
                if IS_VAL[n2] and (s >> VAL_ID[n2]) % 2 and n1 != n2:
                    D[n1][n2][s] += values[n2]

    # now work back in time
    for t in range(3, 27):
        print(t)
        maxval = [[]] * N
        for n1 in range(N):
            maxval[n1] = [[]] * N
            for n2 in range(N):
                maxval[n1][n2] = [0] * V
                for s in range(V):
                    scores = []
                    # option 1: you and elephant both open valve where you are now, respectively
                    if IS_VAL[n1] and IS_VAL[n2] and (s >> VAL_ID[n1]) % 2 and (s >> VAL_ID[n2]) % 2:
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

## correct on example but too slow
def solve2old(nodes, values):
    """D[t][n1][n2][s] with 2 <= t <= 30, n1 and n2 node ids, and 
    s a set of valuable nodes (represented as bitstrings), 
    contains the maximum attainable value with t minutes left, 
    if you are in n1, the elephant is in n2, and the 
    valves in s are still closed."""

    # Initialization, t = 2.
    # All you can do is open the valve where you are now, 
    # if it is still closed, and get 1 minute of pressure out of it.
    D = [[], [], []]
    maxval = [[]] * N
    for n1 in range(N):
        maxval[n1] = [[]] * N
        for n2 in range(N):
            maxval[n1][n2] = [0] * V
            for s in range(V):
                # the valve is still closed, so open it (once)
                if IS_VAL[n1] and (s >> VAL_ID[n1]) % 2:
                    maxval[n1][n2][s] += values[n1]
                if IS_VAL[n2] and (s >> VAL_ID[n2]) % 2 and n1 != n2:
                    maxval[n1][n2][s] += values[n2]
    D[2] = maxval

    # now work back in time
    for t in range(3, 27):
        print(t)
        maxval = [[]] * N
        for n1 in range(N):
            maxval[n1] = [[]] * N
            for n2 in range(N):
                maxval[n1][n2] = [0] * V
                for s in range(V):
                    scores = []
                    # option 1: you and elephant both open valve where you are now, respectively
                    if IS_VAL[n1] and IS_VAL[n2] and (s >> VAL_ID[n1]) % 2 and (s >> VAL_ID[n2]) % 2:
                        myvalve = values[n1] * (t-1)
                        # NB if we do this when we are at the same valve we don't get double the pressure!
                        if n1 == n2:
                            elvalve = 0
                            new_s = s - (1 << VAL_ID[n1])
                        else:
                            elvalve = values[n2] * (t-1)
                            new_s = s - (1 << VAL_ID[n1]) - (1 << VAL_ID[n2]) 
                        scores.append(myvalve + elvalve + D[t-1][n1][n2][new_s])
                    # option 2: you go somewhere else, elephant opens valve
                    if IS_VAL[n2] and (s >> VAL_ID[n2]) % 2:
                        elvalve = values[n2] * (t-1)
                        new_s = s - (1 << VAL_ID[n2])
                        best = max(D[t-1][m][n2][new_s] for m in nodes[n1])
                        scores.append(elvalve + best)
                    # option 3: elephant goes somewhere else, you open valve
                    if IS_VAL[n1] and (s >> VAL_ID[n1]) % 2:
                        myvalve = values[n1] * (t-1)
                        new_s = s - (1 << VAL_ID[n1])
                        best = max(D[t-1][n1][m][new_s] for m in nodes[n2])
                        scores.append(myvalve + best)
                    # option 4: you both go somewhere else
                    scores.append(max(D[t-1][m1][m2][s] for m1 in nodes[n1] for m2 in nodes[n2]))
                    maxval[n1][n2][s] = max(scores)
        D.append(maxval)
    ALL = V - 1
    return D[26][ID["AA"]][ID["AA"]][ALL]


if __name__ == "__main__":
    nodes, values = read("example.txt")
    N = len(nodes)
    valuable = [n for n in range(N) if values[n] != 0]
    IS_VAL = [n in valuable for n in range(N)]
    V = 2 ** len(valuable)
    VAL_ID = {valuable[i]: i for i in range(len(valuable))}
    print(solve2(nodes, values))
