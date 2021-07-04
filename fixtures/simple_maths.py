import pytest


@pytest.fixture
def example_text_numbers():
    return [
        ("two", "three"),
        ("seven", "nine")
    ]


@pytest.fixture
def example_numbers():
    return [(2, 3), (7, 9), (3, 12)]
