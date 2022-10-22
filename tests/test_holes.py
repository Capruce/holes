import pytest

from holes import _


class TestGeneral:
    def test_getattr(self) -> None:
        assert _.a is _.a
        assert _.b is _.b

    def test_incorrect_number_of_arguments(self) -> None:
        with pytest.raises(TypeError):
            ((_.a + _.b)(1))

        with pytest.raises(TypeError):
            ((_.a + _.b)(1, 2, 3))

    def test_holes_do_not_repeat(self) -> None:
        assert (_ + _ + _ + _ + _).holes == (_,)

    def test_holes_are_ordered_by_first_occurrence_left_to_right(self) -> None:
        assert (_.a + _.b).holes == (_.a, _.b)
        assert (_.b + _.a).holes == (_.b, _.a)
        assert (_.a + (_.b + _.a)).holes == (_.a, _.b)
        assert ((_.a + _.b) + _.a).holes == (_.a, _.b)
        assert (_.a + _.b + _.a + _.b).holes == (_.a, _.b)

    def test_arguments_match_order_of_holes(self) -> None:
        f1 = (_.a * 1) + (_.b * 2)
        assert f1(2, 4) == 10

        f2 = (_.b * 2) + (_.a * 1)
        assert f2(2, 4) == 8


class TestAbs:
    def test_abs_hole(self) -> None:
        assert abs(_)(-1) == 1

    def test_abs_lambda(self) -> None:
        assert abs(_ + 1)(-2) == 1


class TestPos:
    def test_pos_hole(self) -> None:
        assert (+_)(-1) == -1

    def test_pos_lambda(self) -> None:
        assert (+(_ + 1))(-2) == -1


class TestNeg:
    def test_neg_hole(self) -> None:
        assert (-_)(-1) == 1

    def test_neg_lambda(self) -> None:
        assert (-(_ + 1))(-2) == 1


class TestAdd:
    def test_hole_add_hole(self) -> None:
        assert (_ + _)(1) == 2

    def test_hole_add_constant(self) -> None:
        assert (_ + 1)(1) == 2

    def test_constant_add_hole(self) -> None:
        assert (1 + _)(1) == 2

    def test_hole_add_lambda(self) -> None:
        assert (_ + (_ + 1))(1) == 3

    def test_lambda_add_hole(self) -> None:
        assert (_ + 1 + _)(1) == 3

    def test_lambda_add_constant(self) -> None:
        assert (_ + 1 + 1)(1) == 3

    def test_constant_add_lambda(self) -> None:
        assert (1 + (_ + 1)) == 3

    def test_lambda_add_lambda(self) -> None:
        assert ((_ + 1) + (_ + 1))(1) == 4


class TestSub:
    def test_hole_sub_hole(self) -> None:
        assert (_ - _)(1) == 0

    def test_hole_sub_constant(self) -> None:
        assert (_ - 1)(1) == 0

    def test_constant_sub_hole(self) -> None:
        assert (1 - _)(1) == 0

    def test_hole_sub_lambda(self) -> None:
        assert (_ - (_ - 1))(1) == 1

    def test_lambda_sub_hole(self) -> None:
        assert (_ - 1 - _)(1) == -1

    def test_lambda_sub_constant(self) -> None:
        assert (_ - 1 - 1)(1) == -1

    def test_constant_sub_lambda(self) -> None:
        assert (1 - (_ - 1)) == 1

    def test_lambda_sub_lambda(self) -> None:
        assert ((_ - 1) - (_ - 1))(1) == 0


class TestMul:
    def test_hole_mul_hole(self) -> None:
        assert (_ * _)(2) == 4

    def test_hole_mul_constant(self) -> None:
        assert (_ * 2)(2) == 4

    def test_constant_mul_hole(self) -> None:
        assert (2 * _)(2) == 4

    def test_hole_mul_lambda(self) -> None:
        assert (_ * (_ * 2))(2) == 8

    def test_lambda_mul_hole(self) -> None:
        assert (_ * 2 * _)(2) == 8

    def test_lambda_mul_constant(self) -> None:
        assert (_ * 2 * 2)(2) == 8

    def test_constant_mul_lambda(self) -> None:
        assert (2 * (_ * 2))(2) == 8

    def test_lambda_mul_lambda(self) -> None:
        assert ((_ * 2) * (_ * 2))(2) == 16


class TestFloorDiv:
    def test_hole_floordiv_hole(self) -> None:
        assert (_ // _)(2) == 1

    def test_hole_floordiv_constant(self) -> None:
        assert (_ // 2)(2) == 1

    def test_constant_floordiv_hole(self) -> None:
        assert (2 // _)(2) == 1

    def test_hole_floordiv_lambda(self) -> None:
        assert (_ // (_ // 2))(2) == 2

    def test_lambda_floordiv_hole(self) -> None:
        assert (_ // 2 // _)(2) == 0

    def test_lambda_floordiv_constant(self) -> None:
        assert (_ // 2 // 2)(2) == 0

    def test_constant_floordiv_lambda(self) -> None:
        assert (2 // (_ // 2))(2) == 2

    def test_lambda_floordiv_lambda(self) -> None:
        assert ((_ // 2) // (_ // 2))(2) == 1


class TestTrueDiv:
    def test_hole_truediv_hole(self) -> None:
        assert (_ / _)(2) == 1.0

    def test_hole_truediv_constant(self) -> None:
        assert (_ / 2)(5) == 2.5

    def test_constant_truediv_hole(self) -> None:
        assert (5 / _)(2) == 2.5

    def test_hole_truediv_lambda(self) -> None:
        assert (_ / (_ / 2))(5) == 2.0

    def test_lambda_truediv_hole(self) -> None:
        assert (_ / 2 / _)(2) == 0.5

    def test_lambda_truediv_constant(self) -> None:
        assert (_ / 2 / 2)(2) == 0.5

    def test_constant_truediv_lambda(self) -> None:
        assert (2 / (_ / 2))(2) == 2.0

    def test_lambda_truediv_lambda(self) -> None:
        assert ((_ / 2) / (_ / 2))(2) == 1.0


class TestPow:
    # ** is right associative
    def test_hole_pow_hole(self) -> None:
        assert (_**_)(2) == 4

    def test_hole_pow_constant(self) -> None:
        assert (_**2)(2) == 4

    def test_constant_pow_hole(self) -> None:
        assert (2**_)(2) == 4

    def test_hole_pow_lambda(self) -> None:
        assert (_**_**2)(2) == 16

    def test_lambda_pow_hole(self) -> None:
        assert ((_**2) ** _)(2) == 16

    def test_lambda_pow_constant(self) -> None:
        assert ((_**2) ** 2)(2) == 16

    def test_constant_pow_lambda(self) -> None:
        assert (2**_**2)(2) == 16

    def test_lambda_pow_lambda(self) -> None:
        assert ((_**2) ** (_**2))(2) == 256


class TestMod:
    def test_hole_mod_hole(self) -> None:
        assert (_ % _)(2) == 0

    def test_hole_mod_constant(self) -> None:
        assert (_ % 2)(3) == 1

    def test_constant_mod_hole(self) -> None:
        assert (3 % _)(2) == 1

    def test_hole_mod_lambda(self) -> None:
        assert (_ % (_ % 2))(3) == 0

    def test_lambda_mod_hole(self) -> None:
        assert (_ % 2 % _)(3) == 1

    def test_lambda_mod_constant(self) -> None:
        assert (_ % 2 % 3)(3) == 1

    def test_constant_mod_lambda(self) -> None:
        assert (3 % (_ % 2))(3) == 0

    def test_lambda_mod_lambda(self) -> None:
        assert ((_ % 2) % (_ % 2))(3) == 0


class TestOther:
    def test_as_lambda_to_map(self) -> None:
        assert list(map(_ * 2, [1, 2, 3])) == [2, 4, 6]

        double = _ * 2
        assert [double(n) for n in [1, 2, 3]] == [2, 4, 6]
