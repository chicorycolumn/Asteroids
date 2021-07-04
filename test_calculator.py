import pytest

from calculator import add, power_to_power, add_text_numbers, multiply_text_numbers
from fixtures.simple_maths import example_text_numbers


@pytest.mark.simple_maths
@pytest.mark.parametrize("a, b, expected", [(1, 5, 6), (4, 99, 103), (-5, 4, -1)])
def test_add_v0(a, b, expected):
    assert add(a, b) == expected


@pytest.mark.simple_maths
@pytest.mark.parametrize("a, b, c, expected", [(2, 3, 4, 4096), (2, 3, 2, 64), (8, 0, 2, 1)])
def test_power_to_power(a, b, c, expected):
    assert power_to_power(a, b, c) == expected


@pytest.mark.simple_maths
def test_add_text_numbers(example_text_numbers):
    assert add_text_numbers(*example_text_numbers[0]) == 5
    assert add_text_numbers(*example_text_numbers[1]) == 16


@pytest.mark.simple_maths
def test_multiply_text_numbers(example_text_numbers):
    assert multiply_text_numbers(*example_text_numbers[0]) == 6
    assert multiply_text_numbers(*example_text_numbers[1]) == 63
