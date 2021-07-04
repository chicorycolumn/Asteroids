import pytest

from calculator import add, power_to_power


@pytest.mark.parametrize("a, b, expected", [(1, 5, 6), (4, 99, 103), (-5, 4, -1)])
def test_add_v0(a, b, expected):
    assert add(a, b) == expected

@pytest.mark.parametrize("a, b, c, expected", [(2, 3, 4, 4096), (2, 3, 2, 64), (8, 0, 2, 1)])
def test_power_to_power(a, b, c, expected):
    assert power_to_power(a, b, c) == expected