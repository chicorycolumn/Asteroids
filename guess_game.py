from random import randint


def play():
    def give_hints(secret_number, guess_number):
        if not secret_number % guess_number:
            print("But my number is divisible by that.")
        if not guess_number % secret_number:
            print("But that is a multiple of my number.")

    secret_number = randint(0, 100)

    print("The games begins! I'm thinking of a number between 1 and 100.")

    while True:
        guess_number = int(input("Please guess:"))

        if guess_number < 0 or guess_number > 100:
            print("No, silly. Between 1 and 100.")
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


if __name__ == "__main__":
    play()
