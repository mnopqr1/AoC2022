NAME = dict()
ID = dict()

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
    """D[t][n][s] with 2 <= t <= 30, n a node id, and s a set of valuable nodes (represented as bitstring), contains the maximum attainable value at time t when starting from node n if the nodes in s are still closed."""
    
    # Initialization, t = 2. 
    # All you can do is open the valve where you are now, if it is still closed, and get 1 minute of pressure out of it.
    D = [[], []]
    maxval = [[]] * N
    for n in range(N):
        maxval[n] = [0] * V
        for s in range(V):
            if n in valuable and (s >> VAL_ID[n]) % 2: # the valve is still closed
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
                    new_s = s - (1 << VAL_ID[n]) # set valve to open
                    scores.append(thisvalve + D[t-1][n][new_s])
                # option 2: go somewhere else
                for m in nodes[n]: # for each neighbor node
                    scores.append(D[t-1][m][s])
                maxval[n][s] = max(scores)
        D.append(maxval)
    ALL = V - 1
    return D[30][ID["AA"]][ALL]

if __name__ == "__main__":
    nodes, values = read("input.txt")
    N = len(nodes)
    valuable = [n for n in range(N) if values[n] != 0]
    V = 2 ** len(valuable)
    VAL_ID = {valuable[i] : i for i in range(len(valuable))}    
    print(solve(nodes, values))