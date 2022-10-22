from abc import ABC, abstractmethod
from typing import TypeAlias, TYPE_CHECKING

if TYPE_CHECKING:
    from .holes import Hole


Context: TypeAlias = dict["Hole", int]


class Expression(ABC):
    @abstractmethod
    def evaluate(self, context: Context) -> int:
        pass


class Constant(Expression):
    def __init__(self, value: int | "Hole") -> None:
        self.value = value

    def evaluate(self, context: Context) -> int:
        if isinstance(self.value, int):
            return self.value
        return context[self.value]


class Add(Expression):
    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def evaluate(self, context: Context) -> int:
        return self.left.evaluate(context) + self.right.evaluate(context)
