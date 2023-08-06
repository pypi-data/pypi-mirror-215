from typing import Callable, Generic, TypeVar

from taipan_di.interfaces import BaseServiceProvider

__all__ = ["FactoryScope"]

T = TypeVar("T")


class FactoryScope(Generic[T]):
    def __init__(self, creator: Callable[[BaseServiceProvider], T]) -> None:
        self._creator = creator

    def get_instance(self, container: BaseServiceProvider) -> T:
        instance = self._creator(container)
        return instance
