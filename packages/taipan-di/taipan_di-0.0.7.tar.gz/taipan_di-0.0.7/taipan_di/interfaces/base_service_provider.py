import abc
from typing import Any, Type, TypeVar, Protocol

__all__ = ["BaseServiceProvider"]

T = TypeVar("T")


class BaseServiceProvider(Protocol):
    """
    The `BaseServiceProvider` contains the services that were registered and allows for
    their resolution via the `resolve` method.
    """

    @abc.abstractmethod
    def contains(self, type: Type[Any]) -> bool:
        """
        Checks if the requested type is registered in the provider's services
        """
        raise NotImplementedError

    @abc.abstractmethod
    def resolve(self, type: Type[T]) -> T:
        """
        Resolve a service along with its dependencies if it is registered in the provider.
        It it isn't, a TaipanUnregisteredError is raised.

        Warning : Depending on how the services were registered, the instance provided might
        not be of the requested type. This would not happen if type hinting is respected.
        """
        raise NotImplementedError
