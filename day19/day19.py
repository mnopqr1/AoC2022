from dataclasses import dataclass
from functools import lru_cache
import sys
from pprint import pprint

debug = True

@dataclass
class Value:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def __eq__(self, other):
        return self.ore == other.ore and self.clay == other.clay and self.obsidian == other.obsidian and self.geode == other.geode
    
    def __hash__(self):
        return self.ore + 100 * self.clay + 10000 * self.obsidian + 1000000 * self.geode

    def __le__(self, other):
        return self.ore <= other.ore and \
               self.clay <= other.clay and \
               self.obsidian <= other.obsidian and \
               self.geode <= other.geode
    
    def __add__(self, other):
        return Value(self.ore + other.ore,
                     self.clay + other.clay,
                     self.obsidian + other.obsidian,
                     self.geode + other.geode)

    def __sub__(self, other):
        return Value(self.ore - other.ore,
                     self.clay - other.clay,
                     self.obsidian - other.obsidian,
                     self.geode - other.geode)

@dataclass
class Cost:
    ore: Value
    clay: Value
    obsidian: Value
    geode: Value

    def __hash__(self):
        return self.ore.__hash__() + 100 * self.clay.__hash__() + 10000 * self.obsidian.__hash__() + 1000000 * self.geode.__hash__()

    def get(self, s):
        if s == "geode": return self.geode
        if s == "obsidian" : return self.obsidian
        if s == "clay": return self.clay
        if s == "ore": return self.ore

SORTS =  ["geode", "obsidian", "clay", "ore"]
ONE = {"ore": Value(1,0,0,0), 
       "clay": Value(0,1,0,0), 
       "obsidian": Value(0,0,1,0), 
       "geode": Value(0,0,0,1),
       "none": Value(0,0,0,0)}

def parse(s: str) -> tuple[int, Cost]:
    ws = s.split(" ")
    n = int(ws[1][:-1])
    rest = [int(ws[i]) for i in [6, 12, 18, 21, 27, 30]]
    cost = Cost(Value(rest[0], 0, 0, 0), 
                Value(rest[1], 0, 0, 0),
                Value(rest[2], rest[3], 0, 0),
                Value(rest[4], 0, rest[5], 0))
    return (n, cost)

def read(filename):
    with open(filename) as f:
        return [parse(line.rstrip()) for line in f.readlines()]

# def decide(inventory, robots, cost):
#     if cost["geode"] <= inventory:
#         return "geode"
#     for sort in ["geode", "obsidian", "clay", "ore"]:
#         if cost[sort] <= inventory:
#             return sort
#     return None

def buy(inv, rs, cost: Cost, purchase):
    price = cost.get(purchase)
    inv = inv - price
    rs = rs + ONE[purchase]
    return inv, rs

@lru_cache(None)
def mostgeodes_aux(inventory, robots, cost: Cost, t) -> int:
    """Returns the max number of geodes that you can crack with t minutes remaining, given the costs, current inventory and robots"""

    #print(f"Looking at what to do in minute {t}.")
    #print(f"Inventory: {inventory}")
    if t == 1:
        return robots.geode

    # choose a robot to buy, if any
    possible = [sort for sort in SORTS if cost.get(sort) <= inventory]
    newinv = Value(inventory.ore, inventory.clay, inventory.obsidian, inventory.geode)
    newrobots = Value(robots.ore, robots.clay, robots.obsidian, robots.geode)
    if "geode" in possible:
        #print("geode possible")
        newinv, newrobots = buy(inventory, robots, cost, "geode")
        newinv = newinv + newrobots - ONE["geode"]
        return robots.geode + mostgeodes_aux(newinv, newrobots, cost, t-1)
    # if "obsidian" in possible:
    #     newinv, newrobots = buy(inventory, robots, cost, "obsidian")
    #     newinv = newinv + newrobots - ONE["obsidian"]
    #     return robots.geode + mostgeodes_aux(newinv, newrobots, cost, t-1)
    
    newinv = newinv + robots
    bestscore = mostgeodes_aux(newinv, robots, cost, t-1)
    
    for sort in possible:
        newinv, newrobots = buy(inventory, robots, cost, sort)
        newinv = newinv + newrobots - ONE[sort]
        score_after_this_purchase = mostgeodes_aux(newinv, newrobots, cost, t-1)
        if score_after_this_purchase > bestscore:
            bestscore = score_after_this_purchase

    return robots.geode + bestscore

def mostgeodes(cost: Cost, T: int) -> int:
    """Return the max number of geodes that you can crack in T minutes."""
    inventory = Value(0, 0, 0, 0)
    robots = Value(1, 0, 0, 0)
    return mostgeodes_aux(inventory, robots, cost, T)

    # for t in range(1,T+1):
    #     print(f"Minute {t}")
    #     print(f"Inventory: {inventory}")
    #     print(f"Robots: {robots}")

    #     purchase = decide(inventory, robots, cost)
    #     if purchase is not None:
    #         print(f"I buy a {purchase} robot.")
    #         inventory, robots = buy(inventory, robots, cost, purchase)
        
    #     inventory = inventory + robots - ONE[purchase]

    # print(f"==Done with this blueprint. Geodes found: {inventory.geode}==")
    # return inventory.geode

def main():
    blueprints = read(sys.argv[1])
    T = 24
    total = 0
    for n, cost in blueprints:
        print(f"==Starting blueprint {n}.==")
        bestscore = mostgeodes(cost, T)
        print(f"Best score: {bestscore}")
        total += n * bestscore
    print(total)

if __name__ == "__main__":
    main()