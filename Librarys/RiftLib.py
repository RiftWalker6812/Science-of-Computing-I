#RiftLib
import math

#Rift_Divisible = lambda a, b: a % b is 0 

def Rift_Divisible(a, b):
    return a % b is 0
def Rift_Divisible(a): #default
    return a % 7 is 0

""" def is_prime(n):
    # Return True if n is a prime number, otherwise False.
    if n <= 1:
        return False  # Numbers <= 1 are not prime
    if n in (2, 3):
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False  # Eliminate even numbers and multiples of 3

    # Check only odd numbers from 5 to sqrt(n), skipping multiples of 2 and 3
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False  # If divisible by i or (i + 2), it's not prime
    return True """

#furthur optimisde with ChatGPT (PYTHON)
def is_prime(n):
    """Return True if n is a prime number, otherwise False."""
    if n < 2 or (n % 2 == 0 and n != 2):
        return False

    if n in (2, 3):  
        return True  

    limit = int(math.sqrt(n))
    return all(n % i != 0 and n % (i + 2) != 0 for i in range(5, limit + 1, 6))