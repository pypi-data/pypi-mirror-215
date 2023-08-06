import abc
from typing import Any, Type, Protocol, TypeVar

from .base_service_provider import BaseServiceProvider
from .base_scope import BaseScope

__all__ = ["BaseServiceContainer"]

T = TypeVar("T")


class BaseServiceContainer(Protocol):
    @abc.abstractmethod
    def contains(self, type: Type[Any]) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def register(self, type: Type[T], service: BaseScope[T]) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def build(self) -> BaseServiceProvider:
        raise NotImplementedError
