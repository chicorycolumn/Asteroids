from random import randint
from games.common import validate_integer


def quick_maths(score: object, cheat: bool = False):
    if cheat:
        print("Cheat mode enabled.")

    answer = None
    num1 = 3 if cheat else randint(1, 50)
    num2 = 3 if cheat else randint(1, 50)

    operator = ["plus", "minus", "multiplied by"][randint(0, 2)]
    if operator == "plus":
        answer = num1 + num2
    elif operator == "minus":
        answer = num1 - num2
    elif operator == "multiplied by":
        answer = num1 * num2

    base_additional_score = 1
    surplus_additional_score = 9

    while True:
        print(f"What is {num1} {operator} {num2}?")

        guess_number = validate_integer(input("Your answer:"))

        if guess_number == None:
            continue

        if guess_number == answer:
            additional_score = base_additional_score + surplus_additional_score
            score["value"] += additional_score
            print(f"Correct! You just scored {additional_score} and your total is {score['value']}")
            break

        if surplus_additional_score:
            surplus_additional_score -= 1

        if guess_number > answer:
            print("Too high!")
            continue

        if guess_number < answer:
            print("Too low!")
            continue
