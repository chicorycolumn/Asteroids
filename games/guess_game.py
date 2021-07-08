from random import randint
from games.common import validate_integer, give_hints


def guess_game(score: object, cheat: bool = False):
    if cheat:
        print("Cheat mode enabled.")

    secret_number = 3 if cheat else randint(1, 50)

    base_additional_score = 1
    surplus_additional_score = 9

    print("The games begins! I'm thinking of a number between 1 and 50.")

    while True:
        guess_number = validate_integer(input("Please guess:"))
        if guess_number == None:
            continue

        if guess_number == secret_number:
            additional_score = base_additional_score + surplus_additional_score
            score["value"] += additional_score
            print(f"You win! You just scored {additional_score} and your total is {score['value']}")
            break

        if surplus_additional_score:
            surplus_additional_score -= 1

        if guess_number < 1 or guess_number > 50:
            print("No, silly. Between 1 and 50.")
            continue

        if guess_number < secret_number:
            print("Too low!")
            give_hints(secret_number, guess_number)
            continue

        if guess_number > secret_number:
            print("Too high!")
            give_hints(secret_number, guess_number)
            continue
