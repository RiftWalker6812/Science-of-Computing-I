#RiftLib
import math

Rift_Divisible = lambda a, b: a % b is 0 

def is_prime(n):
    """Return True if n is a prime number, otherwise False."""
    if n <= 1:
        return False  # Numbers less than or equal to 1 are not prime
    if n == 2:
        return True   # 2 is prime
    if n % 2 == 0:
        return False  # Even numbers greater than 2 are not prime
    for i in range(2, int(math.sqrt(n)) + 1):  # Check up to sqrt(n) for efficiency
        if n % i == 0:
            return False  # Found a divisor, so n is not prime
    return True  # If no divisors were found, n is prime
