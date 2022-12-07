"""Advent of Code Day 7, 2022: a simple file system"""

DIR = 0
FILE = 1

class Directory:
    def __init__(self, name, parent):
        if name != "/": assert parent is not None
        self.name, self.type, self.children, self.parent = name, DIR, [], parent
        if name == "/": 
            self.depth = 0
        else: 
            self.depth = parent.depth + 1
    
    def __str__(self):
        return "-" * self.depth + " " + self.name + "\n" + \
             "\n".join(c.__str__() for c in self.children)  

    def find(self, a):
        # assert a != "/"
        # the following only works because we see the directory a in an "ls" before doing "cd a"
        found = [x for x in self.children if x.type == DIR and x.name == a]
        # assert len(found) == 1
        if len(found) == 1: return found[0]
        else: return None
    
    def add_contents(self, ins, k):
        i = ins[k]
        while i[0] != "$":
            fst, snd = i.split(" ")
            if fst == "dir":
                # assert self.find(words[1]) is None
                self.children.append(Directory(snd, self))
            else:
                self.children.append(File(snd, int(fst), self.depth+1))
            k = k + 1
            if k == len(ins): return k
            i = ins[k]
        return k
    
    def size(self):
        return sum(x.size() for x in self.children)

    def select_dir_sizes(self, cond):
        l = []
        for x in self.children:
            if x.type == DIR:
                l += x.select_dir_sizes(cond)
        if cond(self.size()): l.append(self.size())
        return l

class File:
    def __init__(self, name, size, depth):
        self.name, self.type, self._size, self.depth = name, FILE, size, depth
    
    def size(self):
        return self._size
    
    def __str__(self):
        return "-" * self.depth + " " + self.name + " " + str(self.size())

def build_tree(ins, k, d):
    while k < len(ins):
        i = ins[k]
        if i[0] == "$":
            if i[2:4] == "cd":
                a = i[5:]
                if a == "/":
                    d_to = top
                elif a == "..":
                    d_to = d.parent
                else:
                    d_to = d.find(a)
                k = build_tree(ins, k+1, d_to)
            else:
                # assert i[2:4] == "ls"
                k = d.add_contents(ins, k+1)
    return k

if __name__ == "__main__":
    import sys
    with open(sys.argv[1]) as f:
        ins = [l.rstrip() for l in f.readlines()]

    top = Directory("/", None)
    build_tree(ins, 0, top)

    # part 1
    print(sum(top.select_dir_sizes(lambda x : x < 100000)))

    # part 2
    unused = 70000000 - top.size()
    need = 30000000 - unused
    bigenough = top.select_dir_sizes(lambda x : x > need)
    print(min(bigenough))
