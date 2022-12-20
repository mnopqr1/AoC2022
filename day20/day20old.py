import sys

def read(filename):
    with open(filename) as f:
        xs = [int(l.rstrip()) for l in f.readlines()]
    return xs

def dup(xs):
    for i in range(len(xs)):
        for j in range(i+1,len(xs)):
            if xs[i] == xs[j]:
                print(f"{i}:{xs[i]}, {j}:{xs[j]}")
                return True
    return False

def move(xs, pts, x, i, j, initi):
    """Item x is currently at position i in xs, was initially at index initi. Take it out and insert it at position j. Also update the pointers accordingly."""
    assert xs[i] == x
    xs.pop(i)
    for k in range(i+1,len(pts)):
        pts[k] -= 1
    xs.insert(j, x)
    pts[initi] = j
    for k in range(j+1, len(pts)):
        pts[j+1] += 1

def main():
    initial = read(sys.argv[1])
    # assert not dup(initial)
    N = len(initial)
    # address[i]: where is the element that was initially at index i now?
    address = list(range(N)) 
    mixed = [x for x in initial]
    for i in range(N):
        cur = initial[i]
        curind = address[i]
        newind = curind
        if cur > 0:
            for _ in range(cur):
                if newind == N - 2:
                    newind = 0
                elif newind == N - 1:
                    newind = 1
                else:
                    newind += 1
        else:
            for _ in range(abs(cur)):
                if newind == 1:
                    newind = N - 1
                elif newind == 0:
                    newind = N - 2
                else: newind -= 1
        # newind2 = (curind + cur) % (N - 1)

        assert 0 <= newind < N
        # if newind2 == 0: newind2 = N - 1
        # assert newind == newind2, f"not the same: curind = {curind}, cur = {cur}, newind={newind}, newind2 = {newind2}"
        
        move(mixed, address, cur, curind, newind, i)
        # print(f"{cur} moves to position {newind}, between {mixed[newind-1]} and {mixed[(newind+1)%N]}")
        # print(mixed)
    print(mixed)
    z = mixed.index(0)
    print(mixed[(z + 1000) % N] + mixed[(z + 2000) % N] + mixed[(z + 3000) % N])
        
if __name__ == "__main__":
    main()