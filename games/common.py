import re

def validate_integer(input):
    match = re.match("\d+", str(input))
    if match and str(input) == match.group():
        return int(input)
    else:
        print("Please type a number, with no decimal place.")
        return