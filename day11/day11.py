from dataclasses import dataclass
from typing import List, Callable

debugl = 0
VERB = {"+": "increased", "*": "multiplied"}
MODS = []
N = 0

@dataclass
class Item:
    values: List[int]

    def do(self, op: str, m: str):
        for i, v in enumerate(self.values):
            x = v if m == "old" else int(m)
            if op == "+": self.values[i] = (self.values[i] + x) % MODS[i]
            else: self.values[i] = (self.values[i] * x) % MODS[i]
            if debugl > 0: print(f"   Worry level modulo {MODS[i]} is {VERB[op]} by {x} to {self.values[i]}")
        # self.value = self.value // 3
        # if debug: print(f"   Monkey gets bored with item. Worry level is divided by 3 to {self.value}")

@dataclass
class Monkey:
    id: int
    items: List[Item]
    operation: str
    operand: str
    divisor: int
    iftrue: int
    iffalse: int
    count: int

    def turn(self, monkeys):
        if debugl > 0: print(f"Monkey {self.id}:")
        while len(self.items) > 0:
            self.count += 1
            curr: Item = self.items.pop(0)
            if debugl > 0: print(f"  Monkey inspects an item with a worry level of {curr.values[self.id]} modulo {MODS[self.id]}.")
            curr.do(self.operation, self.operand)
            if curr.values[self.id] % self.divisor == 0:
                if debugl > 0: print(f"    Current worry level is divisible by {self.divisor}.")
                dest = self.iftrue
            else:
                if debugl > 0: print(f"    Current worry level is not divisible by {self.divisor}.")
                dest = self.iffalse
            if debugl > 0: print(f"    The item is thrown to monkey {dest}.")
            monkeys[dest].items.append(curr)

    def __repr__(self):
        return f"Monkey {self.id}: " + ",".join(str(i.values[self.id]) for i in self.items) + f"\nOperation: old = old {self.operation} {self.operand}\nDivisor: {self.divisor}\nIf true: {self.iftrue}\nIf false:{self.iffalse}"


def parse(block):
    rel = [b[b.index(":")+1:] for b in block]
    id = int(block[0].split(" ")[1][:-1])
    its = [Item([int(x) for _ in range(N)]) for x in rel[1].split(",")]
    op, mult = rel[2].split(" ")[4:6]
    div = int(rel[3].split(" ")[-1])
    ift = int(rel[4].split(" ")[-1])
    iff = int(rel[5].split(" ")[-1])
    # print(id, its, op, mult, div, ift, iff)
    return Monkey(id, its, op, mult, div, ift, iff, 0)


def read(filename):
    global MODS
    global N
    with open(filename) as f:
        lines = [l.rstrip().lstrip() for l in f.readlines()]
    N = (len(lines) + 1) // 7
    monkeys: List[Monkey] = []
    for i in range(N):
        monkeys.append(parse(lines[7*i:7*i+6]))
        MODS.append(monkeys[i].divisor)
    return monkeys

def round(monkeys):
    for i in range(len(monkeys)):
        monkeys[i].turn(monkeys)

if __name__ == "__main__":
    monkeys = read("example.txt")
    for i in range(10000):
        if debugl > 0: print(f"== Round {i+1} ==")
        round(monkeys)
        if debugl > 1:
            for m in monkeys:
                print(m)
    cts = sorted(m.count for m in monkeys)
    print(cts[-1]*cts[-2])