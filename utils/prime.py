import math
from typing import List


def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    """
    primes = []
    is_prime = [True] * (n + 1)
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)

            for j in range(i * 2, n + 1, i):
                is_prime[j] = False

    return primes


def sieve_of_eratosthenes_fast(n: int) -> List[int]:
    """
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Algorithm_and_variants
    """
    marks = [False, False] + [True] * (n - 1)

    for i in range(2, math.ceil(math.sqrt(n))):
        if marks[i]:
            for j in range(i ** 2, n + 1, i):
                marks[j] = False

    return [n for (n, m) in enumerate(marks) if m]


def sieve_of_euler(n: int) -> List[int]:
    """
    https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes#Euler's_sieve
    """
    primes = []
    is_prime = [True] * (n+1)
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)

        for p in primes:
            if p * i > n:
                break

            is_prime[p*i] = False

            if i % p == 0:
                break

    return primes
