import unittest
from .. import prime

PRIMES_UNDER_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31,
                    37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]


class TestPrime(unittest.TestCase):
    def test_sieve_of_eratosthenes(self):
        self.assertSequenceEqual(
            prime.sieve_of_eratosthenes(100), PRIMES_UNDER_100)

    def test_sieve_of_eratosthenes_fast(self):
        self.assertSequenceEqual(
            prime.sieve_of_eratosthenes_fast(100), PRIMES_UNDER_100)

    def test_sieve_of_euler(self):
        self.assertSequenceEqual(
            prime.sieve_of_euler(100), PRIMES_UNDER_100)


if __name__ == "__main__":
    unittest.main()
