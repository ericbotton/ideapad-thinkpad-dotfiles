import math
import sys

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

number = int(sys.argv[1])

if is_prime(number):
    print("prime")
else:
    lower = number - 1
    while not is_prime(lower):
        lower -= 1
    print(lower)

    upper = number + 1
    while not is_prime(upper):
        upper += 1
    print(upper)
