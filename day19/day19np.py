from functools import lru_cache
import numpy as np
import sys
from typing import Any


def parse(s: str) -> tuple[int, Any]:
    ws = s.split(" ")
    n = int(ws[1][:-1])
    rest = [int(ws[i]) for i in [6, 12, 18, 21, 27, 30]]
    cost = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                     [-rest[0], 0, 0, 0, 1, 0, 0, 0],
                     [-rest[1], 0, 0, 0, 0, 1, 0, 0],
                     [-rest[2], -rest[3], 0, 0, 0, 0, 1, 0],
                     [-rest[4], 0, -rest[5], 0, 0, 0, 0, 1]])
    return (n, cost)

UPDATE = np.array([
    [1,0,0,0,1,0,0,0],
    [0,1,0,0,0,1,0,0],
    [0,0,1,0,0,0,1,0],
    [0,0,0,1,0,0,0,1],
    [0,0,0,0,1,0,0,0],
    [0,0,0,0,0,1,0,0],
    [0,0,0,0,0,0,1,0],
    [0,0,0,0,0,0,0,1],
])

# how to make a decision on which state to choose next?
EVAL = np.array([
    [0,0,0,0,0,0,0,0]
]).T
def read(filename):
    with open(filename) as f:
        return [parse(line.rstrip()) for line in f.readlines()]

def mostgeodes_aux(state, cost, t):
    if t == 0:
        return 0

    for _ in range(t):
        poss = np.where(np.all(state + cost >= 0, axis=1))[0]
        nextstates = (UPDATE @ state + cost)[poss]
        # print("Possible next states")
        # print(nextstates)
        evals = nextstates @ EVAL
        # print("Evaluations and choice")
        # print(evals)
        choice = len(evals) - 1

        #choice = np.argmax(evals)
        # print(choice)
        state = nextstates[choice]
        
        # print("Update chosen state")
        print(state)
    # best = mostgeodes_aux(UPDATE @ state, cost, t-1)
    # for i in poss:
    #     score = mostgeodes_aux(UPDATE @ state + cost[i], cost, t-1)
    #     if score > best:
    #         best = score
    
    #print(state)
    return state[3]

    state = UPDATE @ state
    
def mostgeodes(cost, T):
    state = np.array([0, 0, 0, 0, 1, 0, 0, 0])

    return mostgeodes_aux(state, cost, T)
    
def main():
    blueprints = read(sys.argv[1])
    T = 24
    total = 0
    for n, cost in blueprints:
        print(f"==Starting blueprint {n}.==")
        # print(cost)
        bestscore = mostgeodes(cost, T)
        print(f"Best score: {bestscore}")
        total += n * bestscore
    print(total)

if __name__ == "__main__":
    main()