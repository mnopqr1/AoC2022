import sys

OPERATION = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x // y,
}
INVL = {
    "+": lambda t, o: t - o,
    "-": lambda t, o: t + o,
    "*": lambda t, o: t // o,
    "/": lambda t, o: t * o
}
INVR = {
    "+": lambda t, o: t - o,
    "-": lambda t, o: o - t,
    "*": lambda t, o: t // o,
    "/": lambda t, o: o // t
}


class Node:
    def __init__(self, name, value, left, right, op):
        self.name = name
        self.value = value
        self.left = left
        self.right = right
        self.op = op

    def contains(self, s):
        return self.name == s or \
            (self.left is not None and self.left.contains(s)) or \
            (self.right is not None and self.right.contains(s))

    def achieve(self, t, s):
        if self.name == s:
            return t
        assert self.op is not None
        if self.left.contains(s):
            oth = self.right.compute()
            tnew = INVL[self.op](t, oth)
            return self.left.achieve(tnew, s)
        else:
            assert self.right.contains(s)
            oth = self.left.compute()
            tnew = INVR[self.op](t, oth)
            return self.right.achieve(tnew, s)

    def compute(self):
        if self.value is not None:
            return self.value
        else:
            return OPERATION[self.op](self.left.compute(), self.right.compute())


def read(filename):
    with open(filename) as f:
        lines = [l.rstrip().split(" ") for l in f.readlines()]
    parsed = dict()
    nodes = dict()
    for l in lines:
        name = l[0][:-1]
        value, leftname, rightname, opname = None, None, None, None
        if len(l) == 2:
            value = int(l[1])
        else:
            leftname, opname, rightname = l[1], l[2], l[3]
        parsed[name] = (value, leftname, rightname, opname)
        nodes[name] = Node(name, value, None, None, None)
    for n in parsed.keys():
        if parsed[n][1] is not None:
            nodes[n].left = nodes[parsed[n][1]]
            nodes[n].right = nodes[parsed[n][2]]
            nodes[n].op = parsed[n][3]
    return nodes


def part2(root):
    target = -1
    if root.left.contains("humn"):
        target = root.right.compute()
    else:
        assert root.right.contains("humn")
        target = root.left.compute()
    print(root.left.achieve(target, "humn"))


def main(filename):
    nodes = read(filename)
    print(nodes["root"].compute())
    part2(nodes["root"])


if __name__ == "__main__":
    main(sys.argv[1])
