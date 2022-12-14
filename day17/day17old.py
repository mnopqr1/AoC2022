import sys

symbol = {0: ".", 1: "#", 2: "+"}
PIECES = {0 : [[1,1,1,1]],
         1 : [[0,1,0], [1,1,1], [0,1,0]],
         2 : [[1,1,1], [0,0,1], [0,0,1]],
         3 : [[1],[1],[1],[1]],
         4 : [[1,1],[1,1]]}
PIECEHEIGHTS = {p: len(PIECES[p]) for p in PIECES.keys()}

def mask(l: list[list[int]]) -> int:
    t = 0
    for y in range(len(l)):
        for x in range(len(l[y])):
            t += l[y][x] << (9 * y + x)
    return t

PIECEMASKS = {p: mask(PIECES[p]) for p in PIECES.keys()}

NEWLINE = mask([[1,0,0,0,0,0,0,0,1]])
MOVES = {"<": -1, ">": +1}
debug = False
wait = False

"""The board is represented as an integer.
It will be 9 wide and h high.
The square at index (y,x) is the bit at position 9 * y + x for any x in [0,8].

"""

if len(sys.argv) > 2 and "-d" in sys.argv[2]:
    debug, wait = True, True

def init():
    return 2 ** 9 - 1, 0

def board_to_str(b: int, bh: int) -> str:
    return "\n".join("".join(symbol[(b >> (9 * y + x)) % 2] for x in range(9)) for y in range(bh-1,-1,-1))

def translate(n: int, x: int, y: int) -> int:
    return n << (9 * y + x)

def spawn(b: int, p: int, h: int, bh: int) -> tuple[int, int, tuple[int,int]]:
    pos = (h + 4, 3)
    pm = PIECEMASKS[p]
    ph = PIECEHEIGHTS[p]
    while bh < pos[0] + ph:
        b |= NEWLINE << (9 * bh)
        bh += 1
    b |= pm << (9 * pos[0] + pos[1])
    return b, bh, pos

def move_to(b, piece, curpos: tuple[int, int], newpos: tuple[int, int]) -> bool:
    cury, curx = curpos
    newy, newx = newpos
    if newx < 0 or newy < 0:
        return False
    for i in range(len(piece)):
        for dx in piece[i]:
            if newx + dx >= WIDTH or b[newy + i][newx + dx] == 1:
                return False
            b[cury + i][curx + dx] = 0
    for i in range(len(piece)):
        for dx in piece[i]:
            b[newy + i][newx + dx] = 2
    return True

def stop_piece(b, piece: list[list[int]], pos: tuple[int,int]):
    cury, curx = pos
    for i in range(len(piece)):
        for dx in piece[i]:
            b[cury + i][curx + dx] = 1

def do_move(b: list[list[int]], p: int, pos: tuple[int,int], move: str):
    dx = MOVES[move]
    cury, curx = pos
    newpos = cury, curx + dx
    piece = PIECES[p]
    if move_to(b, piece, pos, newpos):
        return newpos
    else:
        return pos

def gravity(b: list[list[int]], p: int, pos: tuple[int,int], h: int) -> tuple[tuple[int,int],bool, int]:
    dy = -1
    cury, curx = pos
    newpos = cury + dy, curx
    piece = PIECES[p]
    if move_to(b, piece, pos, newpos):
        return newpos, False, h
    else:
        if cury + len(piece) > h:
            h = cury + len(piece)
        stop_piece(b, piece, pos)
        return pos, True, h

def show(b: int, bh: int):
    print(board_to_str(b, bh))    

ANSWERS = {50_000: 78050, 100_000: 156093}

if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        jet = f.readline().rstrip()
    WIDTH = 7
    INITH = 0
    STOP = 2022
    STOP = 100_000
    STOP = 10_000_000
    board, bh = init() # bh is the height of the board

    J = len(jet) # when to recycle jet list
    c = 1 # how many blocks have been released
    h = 0 # the highest non-moving point so far
    m = 0 # move number
    pos = (-1,-1) # position of the currently moving piece
    stopped = True # whether there is currently a moving piece
    p = 4 # the most recently spawned piece

    i = 0
    while i < STOP:
        i += 1 
    # # for key, piece in PIECEMASKS.items():
    # #     print(board_to_str(piece,4))
    # #     print()
    # i = 0
    # while i < 10_000_000:
    #     board, bh, pos = spawn(board, i % 5, h, bh)
    #     i += 1
    # show(board,bh)
    #show(b,bh)
    # while True:
    #     if stopped:
    #         p = (p + 1) % 5
    #         if c == STOP + 1:
    #             break
    #         #if c % 10_000 == 0 and debug: print(f"Spawn new piece #{c} of type {p}")
    #         pos = spawn(board, p, h, bh)
    #         #print(f"New piece position: {pos}, height: {h}")
    #         c += 1
    #         stopped = False
    #     pos = do_move(board, p, pos, jet[m % J])
    #     m += 1
    #     # if debug:
    #     #     print(f"Move: {jet[m % J]}")
    #     #     print(board_to_str(board))
    #     #     if wait: input()

    #     pos, stopped, h = gravity(board, p, pos, h)
    #     # if debug: 
    #     #     print("Gravity")
    #     #     print(board_to_str(board))
    #     #     if wait: input()

    # if sys.argv[1] == "input.txt" and STOP in ANSWERS.keys():
    #     assert h == ANSWERS[STOP]
    # print(h)

