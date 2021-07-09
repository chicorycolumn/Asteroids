def add(a, b):
    return a + b


def add_text_numbers(a, b):
    return text_to_number(a) + text_to_number(b)


def multiply_text_numbers(a, b):
    return text_to_number(a) * text_to_number(b)


def power_to_power(a, b, c):
    return (a ** b) ** c


def text_to_number(num):
    text_to_number_ref = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "zero": 0,
    }
    if num not in text_to_number_ref:
        raise ValueError(f"Could not translate this text to a number: '{num}'")
    return text_to_number_ref[num]
