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

# Lists out max selection [NOTICE OF REMOVAL OR UPGRADE REQUIRED]
def List_selection_input(max_index):
    """Get user input for selecting an image by index."""
    while True:
        try:
            n = int(input(f"Select an image (0–{max_index}): "))
            if 0 <= n <= max_index:
                return n
            else:
                print(f"Please enter a number between 0 and {max_index}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")
            
def Reverse_Int(n: int, result: int = 0) -> int:
    # Check if input is negative; raise an error if so
    if n < 0:
        raise ValueError("Input must be a non-negative integer")
    
    # Base case: when n becomes 0, return the accumulated result
    if n == 0:
        return result
    
    # Recursive case: extract last digit, shift result, and reduce n
    return Reverse_Int(n // 10, result * 10 + n % 10)

# recursive a new array each time a value gets removed for being lower that the initial, POP
def Get_Arr_Max_Value(arr: list, Max = 0):
    #CHeck
    max = arr[len(arr)-1]
    return Get_Arr_Max_Value()