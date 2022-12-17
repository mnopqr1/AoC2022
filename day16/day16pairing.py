NAME = dict()
ID = dict()
MAXINT = 1_000_000
N: int
ACC: list[list[int]]
FLOWRATE: list[int]
DIST: list[list[int]] # DIST[i][j] is shortest path length from i to j
STEP: list[list[int]] # STEP[i][j] is the next node to go to if you want to get from i to j as fast as possible. we always have step[i][j] in ACC[i]
import sys

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

def roadmap():
    dist = [[]] * N
    step = [[]] * N 
    for i in range(N):
        dist[i] = [MAXINT] * N
        step[i] = [None] * N
        for j in ACC[i]:
            dist[i][j] = 1
            step[i][j] = j
        dist[i][i] = 0
    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    assert step[i][k] is not None
                    step[i][j] = step[i][k]
    return dist, step

def is_in(s, v):
    assert 0 <= v < VS
    return (s >> v) % 2 == 1

def add(s, v):
    assert not is_in(s, v)
    return s + (1 << v)

def single_choice(t, othergoal, pos, opened):
    choice = -1
    best = -1
    potential = [v for v in range(V) if not is_in(opened, v)]
    # if everything is done just make an arbitrary choice
    if len(potential) == 0:
        print(f"No more reasonable goals.")
        return 0
    if len(potential) == 1:
        print(f"One goal left.")
        return VALUABLE[potential[0]]
    for v in potential:
        n = VALUABLE[v]
        if n != othergoal:
            d = DIST[pos][n]
            value = max(t - (d+1), 0) * FLOWRATE[n]
            if value > best:
                best = value
                choice = n
    assert choice != -1, f"for t={t}, other's goal={othergoal}, did not make a choice, open={bin(opened)}"
    return choice
def choose_goals(t, gme, gel, opened, posme, posel) -> tuple[int,int]:
# when I'm in node n at time t, I look at all the closed valves and how far they are from me
# going to a valve of value V which is M minutes away will gain me 
# max(t - (M+1),0) * V points in the end
    if gme is not None and gel is not None:
        return gme, gel
    if gme is None and gel is not None:
        choiceme = single_choice(t, gel, posme, opened)
        return choiceme, gel
    if gel is None and gme is not None:
        choiceel = single_choice(t, gme, posel, opened)
        return gme, choiceel
    assert gel is None and gme is None
    choiceme, choiceel = -1, -1
    potential = [VALUABLE[v] for v in range(V) if not is_in(opened, v)]
    if len(potential) == 0: # nothing more to do
        print(f"No more reasonable goals.")
        return 0, 0
    if len(potential) == 1:
        return potential[0], potential[0]
    scoreme = sorted([(max(t - DIST[posme][n]-1, 0) * FLOWRATE[n], n) for n in potential])
    scoreel = sorted([(max(t - DIST[posel][n]-1, 0) * FLOWRATE[n], n) for n in potential])
    choiceme = scoreme[-1][1]
    choiceel = scoreel[-1][1]
    if choiceel == choiceme:
        if scoreme[-2][0] > scoreel[-2][0]:
            choiceme = scoreme[-2][1]
        else:
            choiceel = scoreel[-2][1]

    return choiceme, choiceel

def solve_aux(t, opened, gme, gel, posme, posel):
    print(f"== {t} Minutes Left ==")
    opennames = ",".join(NAME[VALUABLE[v]] for v in range(V) if is_in(opened,v))
    gains = PRODUCE[opened]
    print(f"Open valves: {opennames}, releasing {gains} pressure")
    if t == 1:
        return PRODUCE[opened]
    
    if posme == gme and gme in VALUABLE and not is_in(opened, VAL_ID[posme]):
        print(f"You open valve {NAME[gme]}.")
        opened = add(opened, VAL_ID[posme])
        gme = None
    else:
        posme = STEP[posme][gme]
        print(f"You move to valve {NAME[posme]}.")
    if posel == gel and gel in VALUABLE and not is_in(opened, VAL_ID[posel]):
        print(f"Elephant opens valve {NAME[gel]}.")
        opened = add(opened, VAL_ID[posel])
        gel = None
    else:
        posel = STEP[posel][gel]
        print(f"Elephant moves to valve {NAME[posel]}.")
    if gme is None or gel is None:
        gme, gel = choose_goals(t, gme, gel, opened, posme, posel)    
    print(f"Your goal: {NAME[gme]}.")
    print(f"Elephant's goal: {NAME[gel]}.")

    return gains + solve_aux(t-1, opened, gme, gel, posme, posel)


def solve(t):
    # returns the best value with t minutes left.
    opened = 0 # nothing open at first
    posme, posel = ID["AA"], ID["AA"]
    
    gme, gel = choose_goals(t, None, None, opened, posme, posel)
    return solve_aux(t, opened, gme, gel, posme, posel)


if __name__ == "__main__":
    
    ACC, FLOWRATE = read(sys.argv[1])
    N = len(ACC)
    DIST, STEP = roadmap()
    for i in range(N):
        STEP[i][i] = i # stay at same node when done

    # print(DIST[ID["DD"]][ID["FF"]], NAME[STEP[ID["DD"]][ID["FF"]]])

    VALUABLE = [n for n in range(N) if FLOWRATE[n] != 0]
    
    # IS_VAL = [n in VALUABLE for n in range(N)]
    V = len(VALUABLE)
    VS = 2 ** V
    VAL_ID = {VALUABLE[i]: i for i in range(len(VALUABLE))}
    # [2,5,9]
    # {2: 0, 5: 1, 9: 2}


    # T = 0

    PRODUCE = [0] * VS
    for s in range(VS):
        PRODUCE[s] = sum(FLOWRATE[v] for i, v in enumerate(VALUABLE) if is_in(s,i))
    print(solve(26))
    # print(PRODUCE[0])
    # print(PRODUCE[V-1])
    #print(solve2old(NODES,VALVES,26))
    #print(solve2rec())
    #test_solve2()
    # t0 = time.time()
    # for t in range(2,27):
    #     answer = solve2rec(t)
    #     #answer = solve2old(NODES,VALVES,t)
    #     # t1 = time.time()
    #     print(f"t={t}, answer={answer}, took {t1-t0} seconds")
    #     t0 = t1