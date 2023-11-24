import math
import sys

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def closest_prime(n):
    if is_prime(n):
        print(f"{n} is a prime number.")
    else:
        lower = n - 1
        upper = n + 1
        while True:
            if is_prime(lower):
                print(f"{n} is not a prime number. The closest prime number is {lower}.")
                break
            elif is_prime(upper):
                print(f"{n} is not a prime number. The closest prime number is {upper}.")
                break
            else:
                lower -= 1
                upper += 1

# Example usage
n = int(input("Enter a number: "))
closest_prime(n)
