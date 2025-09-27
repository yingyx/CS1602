
# Prime Number

import time

def is_prime(n: int) -> bool:
    print(n)
    if n < 2:
        return False
    for k in range(2, n):
        if n % k == 0:
            return False
    return True

def is_prime_optimized(n: int) -> bool:
    if n < 2:
        return False
    for k in range(2, int(n ** 0.5) + 1):
        if n % k == 0:
            return False
    return True

def brute_force(n: int) -> tuple[float, int]:
    t_start = time.time()
    cnt = sum(is_prime(i) for i in range(2, n))
    return time.time() - t_start, cnt

def brute_force_optimized(n: int) -> tuple[float, int]:
    t_start = time.time()
    cnt = sum(is_prime_optimized(i) for i in range(2, n))
    return time.time() - t_start, cnt

def optimized_factor(n: int) -> tuple[float, int]:
    t_start = time.time()
    cnt = 0
    for i in range(5, n):
        if i % 6 == 5 or i % 6 == 1:
            cnt += is_prime_optimized(i)
    cnt += 2 # 2 and 3
    return time.time() - t_start, cnt

def sieve_of_eratosthenes(n: int) -> tuple[float, int]:
    t_start = time.time()
    prime = [True] * n
    prime[0] = prime[1] = False
    for i in range(2, n):
        for j in range(2 * i, n, i):
            prime[j] = False
    cnt = sum(prime)
    return time.time() - t_start, cnt

A = [2, 3]
def is_prime_mr(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    u = n - 1
    t = 0
    while u % 2 == 0:
        u //= 2
        t += 1
    for a in A:
        y = pow(a, u, n)
        if y == 1 or y == n - 1:
            continue
        for _ in range(t):
            y = (y * y) % n
            if y == n - 1:
                break
        else:
            return False
    return True

def miller_rabin(n: int) -> tuple[float, int]:
    t_start = time.time()
    cnt = sum(is_prime_mr(i) for i in range(2, n))
    return time.time() - t_start, cnt

def test_miller_rabin() -> None:
    global A
    A = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 87, 89, 97]
    cases = [1000000000000037, 909091, 99990001, 999999000001, 9999999900000001, 909090909090909091, 1111111111111111111, 11111111111111111111111, 900900900900990990990991]
    for case in cases:
        assert (is_prime_mr(case)) == True
    A = [2, 3]

solutions = {
    # "Brute Force": brute_force, # too time consuming
    "Brute Force Optimized": brute_force_optimized,
    "Optimized Factor": optimized_factor,
    "Sieve of Eratosthenes": sieve_of_eratosthenes,
    "Miller Rabin": miller_rabin,
}

test_miller_rabin()

for sol in solutions:
    result = solutions[sol](1000000)
    print(f"{sol} used {'{:.2f}'.format(result[0])} seconds, giving the result: {result[1]}")
