from typing import (
    Any,
    Callable,
    Generic,
    NoReturn,
    Optional,
    TypeVar,
)


def rraise(_: Any) -> NoReturn:
    raise NotImplementedError


T = TypeVar("T")
INITIAL_T = TypeVar("INITIAL_T")
FINAL_T = TypeVar("FINAL_T")


class Pipe(Generic[INITIAL_T, T]):
    def __init__(
        self, transform: Callable[[INITIAL_T], T], parent: Optional["Pipe"] = None
    ) -> None:
        self.__transform = transform
        self.__parent = parent

    def __rshift__(self, other: Callable[[T], FINAL_T]) -> "Pipe[INITIAL_T, FINAL_T]":
        return Pipe(transform=lambda value: other(self(value)), parent=self)

    def __call__(self, value: INITIAL_T) -> T:
        if self.__parent is None:
            return self.__transform(value)
        else:
            return self.__parent(self.__transform(value))


__all__ = ["Pipe"]
