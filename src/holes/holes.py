from abc import ABC
from typing import Any

from .expressions import Add, Constant, Expression


class Composable(ABC):
    body: Expression

    def __add__(self, right: Any) -> "Lambda":
        if isinstance(right, Composable):
            right_body = right.body
        else:
            right_body = Constant(right)
        return Lambda(Add(self.body, right_body))


class Hole(Composable):
    def __str__(self) -> str:
        return "_"

    @property
    def body(self) -> Expression:
        return Constant(self)


_ = Hole()


class Lambda(Composable):
    def __init__(self, body: Expression) -> None:
        self.body = body

    def __call__(self, argument: int) -> int:
        return self.body.evaluate({_: argument})
