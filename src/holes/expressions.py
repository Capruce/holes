from abc import ABC, abstractmethod
import operator
from typing import TYPE_CHECKING, Callable, ClassVar, TypeAlias, Union

if TYPE_CHECKING:
    from .holes import Hole


Context: TypeAlias = dict["Hole", int]


class Expression(ABC):
    @abstractmethod
    def evaluate(self, context: Context) -> int:
        pass


class Constant(Expression):
    def __init__(self, value: Union[int, "Hole"]) -> None:
        self.value = value

    def evaluate(self, context: Context) -> int:
        from .holes import Hole

        if isinstance(self.value, Hole):
            return context[self.value]
        return self.value


class BinOp(Expression):
    op: Callable[[int, int], int]
    symbol: ClassVar[str]

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def __init_subclass__(cls, op: Callable[[int, int], int], symbol: str) -> None:
        cls.op = op
        cls.symbol = symbol

    def __str__(self) -> str:
        return f"{self.left} {type(self).symbol} {self.right}"

    __repr__ = __str__

    def evaluate(self, context: Context) -> int:
        return type(self).op(
            self.left.evaluate(context),
            self.right.evaluate(context),
        )


class UnaryOp(Expression):
    op: ClassVar[Callable[[int], int]]
    symbol: ClassVar[str]

    def __init__(self, operand: Expression) -> None:
        self.operand = operand

    def __init_subclass__(cls, op: Callable[[int], int], symbol: str) -> None:
        cls.op = op
        cls.symbol = symbol

    def __str__(self) -> str:
        return f"{type(self).symbol}{self.operand}"

    def evaluate(self, context: Context) -> int:
        return type(self).op(self.operand.evaluate(context))


# Arithmetic Operators
class Abs(UnaryOp, op=operator.abs, symbol=""):
    def __str__(self) -> str:
        return f"abs({self.operand})"


class Pos(UnaryOp, op=operator.pos, symbol="+"):
    pass


class Neg(UnaryOp, op=operator.neg, symbol="-"):
    pass


class Add(BinOp, op=operator.add, symbol="+"):
    pass


class Sub(BinOp, op=operator.sub, symbol="-"):
    pass


class Mul(BinOp, op=operator.mul, symbol="*"):
    pass


class FloorDiv(BinOp, op=operator.floordiv, symbol="//"):
    pass


class TrueDiv(BinOp, op=operator.truediv, symbol="/"):
    pass


class MatMul(BinOp, op=operator.matmul, symbol="@"):
    pass


class Pow(BinOp, op=operator.pow, symbol="**"):
    pass


class Mod(BinOp, op=operator.mod, symbol="%"):
    pass


# Comparison
class LT(BinOp, op=operator.lt, symbol="<"):
    pass


class LE(BinOp, op=operator.le, symbol="<="):
    pass


class GT(BinOp, op=operator.gt, symbol=">"):
    pass


class GE(BinOp, op=operator.le, symbol=">="):
    pass


class EQ(BinOp, op=operator.eq, symbol="=="):
    pass


class NE(BinOp, op=operator.ne, symbol="!="):
    pass


# Boolean Operators
class Not(UnaryOp, op=operator.not_, symbol="not"):
    pass


class Inv(UnaryOp, op=operator.inv, symbol="~"):
    pass


class Or(BinOp, op=operator.or_, symbol="|"):
    pass


class And(BinOp, op=operator.and_, symbol="&"):
    pass


class Xor(BinOp, op=operator.xor, symbol="^"):
    pass


# Bitwise
class LShift(BinOp, op=operator.lshift, symbol="<<"):
    pass


class RShift(BinOp, op=operator.rshift, symbol=">>"):
    pass
