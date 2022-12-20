from dataclasses import dataclass
from functools import lru_cache
import sys
from pprint import pprint

debug = True


# @dataclass
# class Cost:
#     ore: Value
#     clay: Value
#     obsidian: Value
#     geode: Value

#     def __hash__(self):
#         return self.ore.__hash__() + 100 * self.clay.__hash__() + 10000 * self.obsidian.__hash__() + 1000000 * self.geode.__hash__()

#     def get(self, s):
#         if s == "geode": return self.geode
#         if s == "obsidian" : return self.obsidian
#         if s == "clay": return self.clay
#         if s == "ore": return self.ore

EXP = {"ore" : 0, "clay" : 4, "obsidian" : 8, "geode" : 16}
INDEX = {"ore" : 0, "clay" : 1, "obsidian" : 2, "geode" : 3}

def value(ore,cl,ob,ge):
    return ore + (cl << 4) + (ob << 8) + (ge << 16)


def get(v: int, sort: str) -> int:
    l = []
    for i in range(4):
        a, v = v % (1 << 4), v >> 4
        l.append(a)
    return l[INDEX[sort]]


def costv(ore, cl, ob, ge):
    return ore + (cl << 16) + (ob << 32) + (ge << 48)

def costget(v: int, sort: str) -> int:
    l = []
    for i in range(4):
        a, v = v % (1 << 16), v >> 16
        l.append(a)
    return l[INDEX[sort]]

SORTS =  ["ore", "clay", "obsidian", "geode"]
ONE = {"ore": value(1,0,0,0), 
       "clay": value(0,1,0,0), 
       "obsidian": value(0,0,1,0), 
       "geode": value(0,0,0,1),
       "none": value(0,0,0,0)}



def parse(s: str) -> tuple[int, int]:
    ws = s.split(" ")
    n = int(ws[1][:-1])
    rest = [int(ws[i]) for i in [6, 12, 18, 21, 27, 30]]
    cost = costv(value(rest[0], 0, 0, 0), 
                value(rest[1], 0, 0, 0),
                value(rest[2], rest[3], 0, 0),
                value(rest[4], 0, rest[5], 0))
    return (n, cost)

def read(filename):
    with open(filename) as f:
        return [parse(line.rstrip()) for line in f.readlines()]

def buy(inv, rs, cost, purchase):
    price = costget(cost, purchase)
    inv = inv - price
    rs = rs + ONE[purchase]
    return inv, rs

@lru_cache(None)
def mostgeodes_aux(inventory: int, robots: int, cost: int, t) -> int:
    """Returns the max number of geodes that you can crack with t minutes remaining, given the costs, current inventory and robots"""

    #print(f"Looking at what to do in minute {t}.")
    #print(f"Inventory: {inventory}")
    if t == 1:
        return get(robots, "geode")

    # choose a robot to buy, if any
    possible = [sort for sort in SORTS if inventory - costget(cost, sort) >= 0]

    newinv, newrobots = inventory, robots
    if "geode" in possible:
        #print("geode possible")
        newinv, newrobots = buy(inventory, robots, cost, "geode")
        newinv = newinv + robots
        return get(robots, "geode") + mostgeodes_aux(newinv, newrobots, cost, t-1)
    # if "obsidian" in possible:
    #     newinv, newrobots = buy(inventory, robots, cost, "obsidian")
    #     newinv = newinv + newrobots - ONE["obsidian"]
    #     return robots.geode + mostgeodes_aux(newinv, newrobots, cost, t-1)
    
    newinv = newinv + robots
    bestscore = mostgeodes_aux(newinv, robots, cost, t-1)
    
    for sort in possible:
        newinv, newrobots = buy(inventory, robots, cost, sort)
        newinv = newinv + robots
        score_after_this_purchase = mostgeodes_aux(newinv, newrobots, cost, t-1)
        if score_after_this_purchase > bestscore:
            bestscore = score_after_this_purchase

    return get(robots, "geode") + bestscore

def mostgeodes(cost: int, T: int) -> int:
    """Return the max number of geodes that you can crack in T minutes."""
    inventory = value(0, 0, 0, 0)
    robots = value(1, 0, 0, 0)
    return mostgeodes_aux(inventory, robots, cost, T)


def main():
    blueprints = read(sys.argv[1])
    T = 19
    total = 0
    n, bp = blueprints[0]
    # for i in range(4):
    #     print(f"Cost of {SORTS[i]}")
    #     cost = costget(bp, SORTS[i])
    #     for s in SORTS:
    #         print(s, get(cost,s))


    # sys.exit()
    for n, cost in blueprints:
        print(f"==Starting blueprint {n}.==")
        bestscore = mostgeodes(cost, T)
        print(f"Best score: {bestscore}")
        total += n * bestscore
    print(total)

if __name__ == "__main__":
    main()