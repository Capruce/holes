from holes import _


def test_add() -> None:
    l = _ + 5
    assert l(5) == 10


def test_hole_add_number():
    add1 = _ + 1
    assert add1(1) == 2


def test_number_add_hole():
    add1 = 1 + _
    assert add1(1) == 2


def test_hole_add_hole():
    double = _ + _
    assert double(1) == 2
