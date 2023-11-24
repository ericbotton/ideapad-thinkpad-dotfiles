import math

def perfect_square():
    num = input("Enter a number: ")
    try:
        num = float(num)
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        exit()
    
    root = math.sqrt(num)
    if int(root + 0.5) ** 2 == num:
        print(f"{num} is a perfect square.")
    else:
        lower_square = math.floor(root) ** 2
        higher_square = math.ceil(root) ** 2
        print(f"{num} is not a perfect square.")
        print(f"The next lower perfect square is {lower_square}.")
        print(f"The next higher perfect square is {higher_square}.")

perfect_square()
