from random import randint
from games.common import validate_integer


def quick_maths():
    answer = None
    num1 = randint(1, 50)
    num2 = randint(1, 50)
    operator = ["plus", "minus", "multiplied by"][randint(0, 2)]
    if operator == "plus":
        answer = num1 + num2
    elif operator == "minus":
        answer = num1 - num2
    elif operator == "multiplied by":
        answer = num1 * num2

    while True:
        print(f"What is {num1} {operator} {num2}?")

        guess_number = validate_integer(input("Your answer:"))
        if guess_number == None:
            continue

        if guess_number > answer:
            print("Too high!")
            continue

        if guess_number < answer:
            print("Too low!")
            continue

        if guess_number == answer:
            print("Correct!")
            break
