
# 1. Tower of Hanoi

def move(src: str, tar: str) -> None: # only adjacent moves
    assert is_adjacent(src, tar)
    print(f"{src}->{tar}")
        
def is_adjacent(src: str, tar: str) -> bool:
    return not ((src == 'A' and tar == 'C') or (src == 'C' and tar == 'A'))

def hanoi_plus(n: int, x: str, y: str, z: str) -> None:
    '''
    :param n int: the number of disks
    :param x str: the name of the source rod
    :param y str: the name of the spare rod
    :param z str: the name of the target rod
    '''
    if n == 0:
        return
    if is_adjacent(x, z):
        hanoi_plus(n - 1, x, z, y)
        move(x, z)
        hanoi_plus(n - 1, y, x, z)
    else:
        hanoi_plus(n - 1, x, y, z)
        move(x, y)
        hanoi_plus(n - 1, z, y, x)
        move(y, z)
        hanoi_plus(n - 1, x, y, z)
        
    
hanoi_plus(1, 'A', 'B', 'C')
print()
hanoi_plus(2, 'A', 'B', 'C')
print()
hanoi_plus(3, 'A', 'B', 'C')
print()

# 2. The Josephus Problem

## 2.1. First Problem

def circle(n: int) -> int:
    s = list(range(1, n+1))
    curr = 1
    while len(s) > 1:
        s.pop(curr)
        curr = (curr + 1) % len(s)
    return s[0]

print(circle(1))
print(circle(2))
print(circle(3))
print(circle(4))
print(circle(10))
print()

## 2.2. Second Problem

def circle2(n: int) -> int:
    if n == 1:
        return 1
    return 2 * circle2(n // 2) + (1 if n % 2 else -1)

print(circle2(1))
print(circle2(2))
print(circle2(3))
print(circle2(4))
print(circle2(10))
print()

## 2.3. Third Problem

import math
def circle3(n: int) -> int:
    return 2 * (n - 2 ** math.floor(math.log2(n))) + 1

print(circle3(1))
print(circle3(2))
print(circle3(3))
print(circle3(4))
print(circle3(10))
print()

# 3. 棋盘问题

off = [[(0, 0), (1, 0), (0, 1)], [(0, 0), (0, -1), (1, 0)],
       [(0, 0), (-1, 0), (0, 1)], [(0, 0), (-1, 0), (0, -1)]]

def solve(map: list[list[int]]):
    w, h = len(map[0]), len(map)
    if not any(map[i][j] == 0 for i in range(h) for j in range(w)):
        return map
    
    for i in range(h):
        for j in range(w):
            for k, o in enumerate(off):
                if not any(i + _[0] < 0 or i + _[0] >= h or j + _[1] < 0 or j + _[1] >= w or map[i + _[0]][j + _[1]] for _ in o):
                    for __ in o:
                        map[i + __[0]][j + __[1]] = k + 1
                    if solve(map):
                        return solve(map)
                    for __ in o:
                        map[i + __[0]][j + __[1]] = 0
                        
print(solve([[0, 100, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))
