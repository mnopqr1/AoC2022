import sys
with open(sys.argv[1]) as f:
    ins = [l.rstrip() for l in f.readlines()]

DIR = 0
FILE = 1
top = []

def find_inside(t,a):
    for x in t:
        if x[0] == DIR: 
            d = find_dir(x[2], a)
            if d is not None: return d
            d = find_inside(x[2], a)
            if d is not None: return d
    assert False, "not found"
    
def find_dir(t, a):
    assert a != "/"
    found = [x for x in t if x[0] == DIR and x[1] == a]
    assert len(found) <= 1
    if len(found) == 1: return found[0]
    else: return None

def add_contents(ins, k, t, parent):
    i = ins[k]
    while i[0] != "$":
        print(k, i, t, sep=", ")
        words = i.split(" ")
        if words[0] == "dir":
            assert find_dir(t,words[1]) is None
            t.append((DIR, words[1], [], parent))
        else:
            t.append((FILE, int(words[0]), words[1], parent))
        k = k + 1
        i = ins[k]
    return k

def build_tree(ins, k, t, curdir):
    while k < len(ins):
        i = ins[k]

        print(k, i, t, curdir, sep=", ")
        print("Toplevel:", top)
        if i[0] == "$":
            if i[2:4] == "cd":
                a = i[5:]
                if a == "/":
                    k = build_tree(ins, k+1, top, "/")
                elif a == "..":
                    d = find_inside(top, curdir[3])
                    k = build_tree(ins, k+1, d, curdir[3])
                else:
                    d = find_dir(t, a)
                    k = build_tree(ins, k+1, d[2], a)
            else:
                assert i[2:4] == "ls"
                k = add_contents(ins, k+1, t, curdir)

build_tree(ins, 0, top, "/")
print(top)
