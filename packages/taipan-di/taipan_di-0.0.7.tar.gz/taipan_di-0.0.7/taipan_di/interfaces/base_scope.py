import abc
from typing import TypeVar, Protocol

from .base_service_provider import BaseServiceProvider

__all__ = ["BaseScope"]

T = TypeVar("T", covariant=True)


class BaseScope(Protocol[T]):
    @abc.abstractmethod
    def get_instance(self, container: BaseServiceProvider) -> T:
        raise NotImplementedError()
