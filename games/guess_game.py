from random import randint
from games.common import validate_integer


def guess_game():
    def give_hints(secret_number, guess_number):
        if guess_number == 1:
            return
        if not secret_number % guess_number:
            print("But my number is divisible by that.")
        if not guess_number % secret_number:
            print("But that is a multiple of my number.")

    secret_number = randint(1, 50)
    print("The games begins! I'm thinking of a number between 1 and 50.")

    while True:
        guess_number = validate_integer(input("Please guess:"))
        if guess_number == None:
            continue

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

        if guess_number == secret_number:
            print("You win!")
            break
