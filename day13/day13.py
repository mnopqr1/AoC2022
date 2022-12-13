DL = 0
from functools import cmp_to_key

def find_closing(s:str, i:int):
    assert s[i] == "["
    k = i + 1
    d = 1
    while d != 0:
        if s[k] == "[":
            d += 1
        if s[k] == "]":
            d -= 1
        k += 1
    return k

def parse_list(s:str):
    if s == "": return ""
    assert s[0] == "["
    i = 1
    r = []
    #print("s: ", s)

    while i < len(s) and s[i] != "]":
        if s[i] == "[":
            next = find_closing(s,i)
            r.append(parse_list(s[i:next]))
        else:
            next = s.find(",",i)
            if next == -1: next = s.find("]", i)
            r.append(int(s[i:next]))
        i = next + 1
    return r


def read(filename):
    with open(filename) as f:
        ls = [parse_list(l.rstrip()) for l in f.readlines()]
        pairs = [(ls[i],ls[i+1]) for i in range(0,len(ls),3)]
    return pairs

def compare(l,r):
    if str(l).isnumeric() and str(r).isnumeric():
        if DL > 0: print(f"Comparing {l} and {r} (numeric)")
        if l < r:
            if DL > 0: print(f"{l} is smaller than {r}, right order, return True")
            return "T"
        elif l > r:
            if DL > 0: print(f"{r} is smaller than {l}, not right order, return False")
            return "F"
        else:
            if DL > 0: print(f"{l} equals {r}, return Equal")
            return "E"

    if not str(l).isnumeric() and not str(r).isnumeric():
        if DL > 0: print(f"Comparing {l} and {r} (lists)")
        c = 0
        while c < min(len(l),len(r)):
            res = compare(l[c],r[c])
            if res in ["T","F"]:
                return res
            c += 1
        if DL > 0: print(f"List comparison ended, return {len(l)} < {len(r)}")
        if len(l) < len(r):
            return "T"
        if len(l) > len(r):
            return "F"
        return "E"
    if str(l).isnumeric() and not str(r).isnumeric():
        if DL > 0: print(f"Mixed types; convert left to {[l]} and retry comparison.")
        return compare([l],r)
    if not str(l).isnumeric() and str(r).isnumeric():
        if DL > 0: print(f"Mixed types; convert right to {[r]} and retry comparison.")
        return compare(l,[r])

def compint(a,b):
    if compare(a,b) == "T":
        return -1
    if compare(a,b) == "F":
        return 1
    return 0

if __name__ == "__main__":
    pairs = read("input.txt")
    t = 0
    # part 1
    for i, pair in enumerate(pairs):
        v = i + 1
        if DL > 0: print(f"==Pair {v}==")
        if compare(pair[0],pair[1]) == "T":
            t += v
        if DL > 0: print()
    print(t)
    
    # part 2
    packets = [p[0] for p in pairs] + [p[1] for p in pairs] + [ [[2]], [[6]] ]
    packets.sort(key=cmp_to_key(compint))
    for p in packets:
        if DL > 0: print(p)
    print((packets.index([[2]])+1) * (packets.index([[6]])+1))