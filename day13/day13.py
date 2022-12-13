from functools import cmp_to_key


def find_closing(s:str, i:int):
    k, d = i + 1, 1
    while d != 0:
        if s[k] == "[": d += 1
        if s[k] == "]": d -= 1
        k += 1
    return k


def parse_list(s:str):
    if s == "": return ""
    i, r = 1, []

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


def isint(x):
    return str(x).isnumeric()


def compare(l,r):
    if isint(l) and isint(r):
        if l < r: return -1
        if l > r: return 1
        return 0
    if not isint(l) and not isint(r):
        c = 0
        while c < min(len(l),len(r)):
            res = compare(l[c],r[c])
            if res != 0: return res
            c += 1
        return compare(len(l),len(r))
    if isint(l) and not isint(r):
        return compare([l],r)
    if not isint(l) and isint(r):
        return compare(l,[r])


if __name__ == "__main__":
    pairs = read("input.txt")
    
    # part 1
    t = 0
    for i, (l,r) in enumerate(pairs):
        v = i + 1
        if compare(l,r) == -1:
            t += v
    print(t)
    
    # part 2
    packets = [p[0] for p in pairs] + [p[1] for p in pairs] + [ [[2]], [[6]] ]
    packets.sort(key=cmp_to_key(compare))
    print((packets.index([[2]])+1) * (packets.index([[6]])+1))