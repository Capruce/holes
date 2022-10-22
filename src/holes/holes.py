from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from functools import cache
from typing import Literal, TypeAlias, Union, overload

from .expressions import (
    EQ,
    GE,
    GT,
    LE,
    LT,
    NE,
    Abs,
    Add,
    And,
    BinOp,
    Constant,
    Expression,
    FloorDiv,
    Inv,
    LShift,
    MatMul,
    Mod,
    Mul,
    Neg,
    Or,
    Pos,
    Pow,
    RShift,
    Sub,
    TrueDiv,
    UnaryOp,
    Xor,
)

Value: TypeAlias = Union[int, "Composable"]
BinaryDunder: TypeAlias = Callable[["Composable", Value], "Lambda"]
UnaryDunder: TypeAlias = Callable[["Composable"], "Lambda"]


def unaryop(cls: type[UnaryOp]) -> UnaryDunder:
    def dunder(self: "Composable") -> "Lambda":
        return Lambda(self.holes, cls(self.body))

    return dunder


@overload
def binop(cls: type[BinOp], has_reverse: Literal[False]) -> BinaryDunder:
    ...


@overload
def binop(
    cls: type[BinOp],
    has_reverse: Literal[True] = ...,
) -> tuple[BinaryDunder, BinaryDunder]:
    ...


def binop(
    cls: type[BinOp],
    has_reverse: bool = True,
) -> tuple[BinaryDunder, BinaryDunder] | BinaryDunder:
    def dunder(self: "Composable", right: Value) -> "Lambda":
        if isinstance(right, Composable):
            holes = right.holes
            body = right.body
        else:
            holes = []
            body = Constant(right)

        return Lambda([*self.holes, *holes], cls(self.body, body))

    def rdunder(self: "Composable", left: Value) -> "Lambda":
        if isinstance(left, Composable):
            holes = left.holes
            body = left.body
        else:
            holes = []
            body = Constant(left)

        return Lambda([*holes, *self.holes], cls(body, self.body))

    if has_reverse:
        return dunder, rdunder
    return dunder


class Composable(ABC):
    __abs__ = unaryop(Abs)
    __pos__ = unaryop(Pos)
    __neg__ = unaryop(Neg)

    __add__, __radd__ = binop(Add)
    __sub__, __rsub__ = binop(Sub)
    __mul__, __rmul__ = binop(Mul)
    __matmul__, __rmatmul__ = binop(MatMul)
    __floordiv__, __rfloordiv__ = binop(FloorDiv)
    __truediv__, __rtruediv__ = binop(TrueDiv)
    __pow__, __rpow__ = binop(Pow)
    __mod__, __rmod__ = binop(Mod)

    __lt__ = binop(LT, has_reverse=False)
    __le__ = binop(LE, has_reverse=False)
    __gt__ = binop(GT, has_reverse=False)
    __ge__ = binop(GE, has_reverse=False)
    __eq__ = binop(EQ, has_reverse=False)  # type: ignore[assignment]
    __ne__ = binop(NE, has_reverse=False)  # type: ignore[assignment]

    __invert__ = unaryop(Inv)
    __lshift__, __rlshift__ = binop(LShift)
    __rshift__, __rrshift__ = binop(RShift)
    __and__, __rand__ = binop(And)
    __or__, __ror__ = binop(Or)
    __xor__, __rxor__ = binop(Xor)

    @property
    @abstractmethod
    def body(self) -> Expression:
        ...

    @property
    @abstractmethod
    def holes(self) -> Sequence["Hole"]:
        ...


class Hole(Composable):
    def __init__(self, name: str) -> None:
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Hole({self.name})"

    @property
    def body(self) -> Expression:
        return Constant(self)

    @property
    def holes(self) -> Sequence["Hole"]:
        return [self]

    def __hash__(self) -> int:
        return hash(self.name)

    def __getattr__(self, name: str) -> "Hole":
        try:
            return _NAME_TO_HOLE[name]
        except KeyError:
            hole = _NAME_TO_HOLE[name] = Hole(name)
            return hole


_NAME_TO_HOLE: dict[str, Hole] = {}


_ = Hole("_")


def dedup(holes: Sequence[Hole]) -> tuple[Hole, ...]:
    seen = set()
    output = []
    for hole in holes:
        if hole in seen:
            continue
        seen.add(hole)
        output.append(hole)
    return tuple(output)


class Lambda(Composable):
    def __init__(self, holes: Sequence[Hole], body: Expression) -> None:
        self._holes = dedup(holes)
        self._body = body

    @property
    def holes(self) -> Sequence[Hole]:
        return self._holes

    @property
    def body(self) -> Expression:
        return self._body

    def __str__(self) -> str:
        return f"lambda _: {self.body}"

    def __call__(self, *args: int) -> int:
        if len(args) != len(self.holes):
            raise TypeError()

        context = dict(zip(self.holes, args))
        return self.body.evaluate(context)
