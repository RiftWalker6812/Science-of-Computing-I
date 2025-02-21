import sys
import os
# Get the directory containing 'library'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# additional librarys
import time
from Librarys.RiftLib import is_prime

# Gets Input
while True:
    try:
        N = int(input("Give me a number between 1 and 100, OR ELSE: "))
        if 101 <= N:
            continue
        break
    except ValueError as e:
        print(f"{e} try again")

# Starting time collection
start_Time = time.time()

# Initial array
a = [[i for i in range(1, N + 1)], [0] * N]
print(f"{a[0]}\n{a[1]}\n")

# Checks for primes
i = 0
for i in range(N):
    if is_prime(i):
        a[1][i] = 1
        if N > i*2:
            a[1][i*2] = 1

# Gets the final variables and ends time calculation
largest_prime = max([num for num in a[0] if is_prime(num)])
End_Time = time.time()
Elapsed_Time = End_Time - start_Time

# Prints Data
print(a[0], a[1], sep="\n")
print(f"The Time it took for the calculations: {Elapsed_Time} Seconds \nThe largest prime is: {largest_prime}")
