import re


def validate_integer(input):
    match = re.match("\d+", str(input))
    if match and str(input) == match.group():
        return int(input)
    else:
        print("Please type a number, with no decimal place.")
        return


def give_hints(secret_number, guess_number):
    if guess_number == 1:
        return
    if not secret_number % guess_number:
        print("But my number is divisible by that.")
    if not guess_number % secret_number:
        print("But that is a multiple of my number.")
