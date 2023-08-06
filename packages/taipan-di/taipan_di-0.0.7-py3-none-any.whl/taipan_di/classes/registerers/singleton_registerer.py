from typing import Callable, Type, Generic, TypeVar

from taipan_di.classes.scopes import SingletonScope
from taipan_di.classes.tools import instanciate_service

from taipan_di.interfaces import BaseServiceProvider, BaseServiceContainer

__all__ = ["SingletonRegisterer"]

T = TypeVar("T")


class SingletonRegisterer(Generic[T]):
    """
    Part of the registration process.

    You shouldn't have to create instances of this class by yourself.
    """

    def __init__(
        self, type_to_register: Type[T], container: BaseServiceContainer
    ) -> None:
        self._type_to_register = type_to_register
        self._container = container

    def with_implementation(self, implementation_type: Type[T]) -> None:
        """
        Register the service as a singleton with `implementation_type` as its implementation.

        Resolving the service will return an instance of `implementation_type`.
        """

        creator = lambda provider: instanciate_service.instanciate_service(
            implementation_type, provider
        )
        self._register(creator)

    def with_creator(self, creator: Callable[[BaseServiceProvider], T]) -> None:
        """
        Register the service as a singleton with the specified creator..
        """

        self._register(creator)

    def with_instance(self, instance: T) -> None:
        """
        Register the service as a singleton with `instance` as its registered instance.

        Resolving the service will return `instance`.
        """

        creator = lambda provider: instance
        self._register(creator)

    def with_self(self) -> None:
        """
        Register the service as a singleton with itself as its implementation.

        Resolving the service will return an instance of itself.
        """

        creator = lambda provider: instanciate_service.instanciate_service(
            self._type_to_register, provider
        )
        self._register(creator)

    def _register(self, creator: Callable[[BaseServiceProvider], T]) -> None:
        scope = SingletonScope[T](creator)
        self._container.register(self._type_to_register, scope)
