import pytest

from src.primarymath import number


def test_should_return_the_right_value():
    expected = 4
    n = number.Number(4)
    assert n.value == expected


def test_previous_value():
    expected = 183
    n = number.Number(184)
    assert n.previous() == expected


def test_next_value():
    expected = 524
    n = number.Number(523)
    assert n.next() == expected


def test_is_positive_should_be_false():
    expected = False
    n = number.Number(-17)
    assert n.is_positive() == expected


def test_is_positive_should_be_true():
    expected = True
    n = number.Number(1127)
    assert n.is_positive() == expected


def test_is_even_should_be_false():
    expected = False
    n = number.Number(131)
    assert n.is_even() == expected


def test_is_even_should_be_true():
    expected = True
    n = number.Number(48)
    assert n.is_even() == expected
