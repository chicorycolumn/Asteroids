import pytest

from abacus import Abacus
from fixtures.simple_maths import example_numbers


@pytest.fixture
def abacus():
    return Abacus()


@pytest.mark.simple_maths
def test_is_multiple(abacus, example_numbers):
    assert abacus.is_multiple(*example_numbers[0]) is False
    assert abacus.is_multiple(*example_numbers[1]) is False
    assert abacus.is_multiple(*example_numbers[2]) is True


@pytest.mark.simple_maths
@pytest.mark.parametrize("a, b, expected", [(2, 4, 16), (3, 2, 9), (5, 3, 125)])
def test_to_power(abacus, a, b, expected):
    assert abacus.to_power(a, b) == expected
