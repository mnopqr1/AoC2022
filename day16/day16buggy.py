import copy
from functools import lru_cache
import sys
from typing import Optional
from copy import deepcopy

dc = deepcopy
NAME = dict()
ID = dict()
N: int
ACC: list[list[int]]
VALUE: list[int]
MAXINT = 1_000_000

def str_of_node(i: int) -> str:
    return f"Node {i} (={NAME[i]}), value {VALUE[i]}, tunnels to: {ACC[i]}"

def read(filename):
    with open(filename) as f:
        lines = [l for l in f.readlines()]
    N = len(lines)
    ACC, VALUE = [[]] * N, [0] * N
    c = 0
    for l in lines:
        ws = l.split(" ")
        currname, value, accnames = ws[1], int(ws[4][5:-1]), [n[:-1] for n in ws[9:]]
        for n in [currname] + accnames:
            if n not in ID.keys():
                ID[n], NAME[c] = c, n
                c += 1
        VALUE[ID[currname]], ACC[ID[currname]] = value, [ID[n] for n in accnames]
    assert c == N and all(NAME[ID[n]] == n for n in ID.keys())
    return ACC, VALUE, ID, NAME, N

class State:
    open: list[int]

    def __init__(self):
        self.open = []

    def is_open(self, i):
        return i in self.open
    
    def open_up(self, i):
        assert i not in self.open, f"Trying to open up a valve that is already open"
        assert VALUE[i] > 0, f"Trying to open up a valve that has zero value"
        self.open.append(i)
    
    @lru_cache()
    def ppm(self):
        """Pressure per minute in this state"""
        return sum(VALUE[i] for i in self.open)
    
    def __str__(self):
        return self.open.__str__()

class Agent:
    id: int
    position: int
    goal: Optional[int]

    def __init__(self, id, pos, goal):
        self.id = id
        self.position = pos
        self.goal = goal

    def set_goal(self, g):
        assert VALUE[g] > 0
        self.goal = g
    
    def __str__(self):
        return f"Agent id: {self.id}, pos: {self.position}, goal: {self.goal}"

@lru_cache(None)
def highestpressure(t, a1, a2, s):
    """Highest attainable pressure with t minutes left and agents a1, a2 with valves in state s."""
    print(f"Finding highest attainable pressure for t = {t} {a1},{a2}, currently open = {s}")
    if t <= 0:
        return 0
    pressure_now = s.ppm()
    if t == 1:
        return pressure_now
    

    ags = [a1,a2]
    need_goals = []
    for a in ags:
        assert a.goal is not None
        if a.position == a.goal:
            s.open_up(a.goal)
            a.goal = None
            need_goals.append(a)
        else:
            a.position = STEP[a.position][a.goal]
    
    current_goals = [a.goal for a in ags if a not in need_goals]
    
    bestscore = 0
    if len(need_goals) == 0:
        bestscore = highestpressure(t-1, dc(a1), dc(a2), dc(s))
        print(f"No new goals set for t={t}, open={s}, best score {bestscore}")
    else:
        potential = [i for i in range(N) if VALUE[i] > 0 and not s.is_open(i) and not i in current_goals]
        if len(need_goals) == 1:
            ame, = need_goals
            aoth = [a for a in ags if a.goal is not None][0]
            for p in potential:
                print(f"Setting new goal for Agent {ame.id} to {p}")
                ame.set_goal(p)
                score = highestpressure(t-1,dc(ame),dc(aoth),dc(s)) 
                if score > bestscore:
                    bestscore = score
        else:
            for i, p in enumerate(potential):
                for j in range(i+1,len(potential)):
                    a1new, a2new = a1, a2
                    print(f"Setting goal for Agent {a1new.id} to {p}")
                    a1new.set_goal(p)
                    q = potential[j]
                    print(f"Setting goal for Agent {a2new.id} to {q}")
                    a2new.set_goal(q)
                    score = highestpressure(t-1, dc(a1new), dc(a2new), dc(s))
                    if score > bestscore:
                        bestscore = score
    print(f"returning highest found pressure for t={t}: {pressure_now+bestscore}")
    return pressure_now + bestscore

def solve(t):
    best = 0
    for i in range(N):
        if VALUE[i] == 0: continue
        for j in range(i+1,N):
            if VALUE[j] == 0: continue
            print(f"===Initial goal for Agent 1: {i}, for Agent 2: {j}===")
            a1 = Agent(1, ID["AA"], i)
            a2 = Agent(2, ID["AA"], j)
            s = State()
            t0 = t
            score = highestpressure(t0, a1, a2, s)
            if score > best:
                best = score
    return best
    
def roadmap():
    dist = [[]] * N
    step = [[]] * N # step[i][j] is the next node to go to if you want to get from i to j as fast as possible. we always have step[i][j] in ACC[i]
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


if __name__ == "__main__":
    filename = sys.argv[1]
    ACC, VALUE, ID, NAME, N = read(filename)
    DIST, STEP = roadmap()
    # for i in range(N):
    #     for j in range(i+1,N):
    #         print(f"From {i} to {j}, a path of length {DIST[i][j]}:")
    #         k = i
    #         while k != j:
    #             print(f"Step from {k} to {STEP[k][j]}")
    #             k = STEP[k][j]
    print(solve(26))
