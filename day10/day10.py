from typing import Optional

NOOP, ADDX = 1, 2
NAME = {NOOP: "noop", ADDX: "addx"}

class Instruction:
    type: str
    value: int

    def __init__(self, type: int, value: Optional[int]=None):
        if type == NOOP: assert value == None
        self.type = type
        self.value = value
    
    def __repr__(self):
        return f"{NAME[self.type]}, {self.value}"
        
def parse(l):
    ws = l.split(" ")
    if len(ws) > 1:
        assert len(ws) == 2 and ws[0] == "addx"
        return Instruction(ADDX, int(ws[1]))
    else:
        assert len(ws) == 1 and ws[0] == "noop"
        return Instruction(NOOP)

def read(filename):
    with open(filename) as f:
        ins = [parse(l.rstrip()) for l in f.readlines()]
    return ins

def execute(ins):
    trace = [] # trace[i] is the register value during the i+1th cycle
    c = 1
    for i in ins:
        if i.type == NOOP:
            trace.append(c)
        else:
            trace += [c,c]
            c += i.value
    return trace

def q1(trace):
    for k in range(20,221,40):
        print(f"{k}, {trace[k-1]}")
    return sum(k * trace[k-1] for k in range(20,221,40))

if __name__ == "__main__":
    ins = read("input.txt")
    trace = execute(ins)
    #print(trace)
    print(q1(trace))
    #print("\n".join(i.__repr__() for i in ins))
