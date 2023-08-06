from typing import Type, TypeVar, Generic

from taipan_di.interfaces import BaseServiceContainer

from .singleton_registerer import SingletonRegisterer
from .factory_registerer import FactoryRegisterer

__all__ = ["ServiceRegisterer"]


T = TypeVar("T")


class ServiceRegisterer(Generic[T]):
    """
    Part of the registration process.

    You shouldn't have to create instances of this class by yourself.
    """

    def __init__(
        self, type_to_register: Type[T], container: BaseServiceContainer
    ) -> None:
        self._type_to_register = type_to_register
        self._container = container

    def as_singleton(self) -> SingletonRegisterer[T]:
        """
        Continue the registration process of the service as a singleton.
        """

        registerer = SingletonRegisterer[T](self._type_to_register, self._container)
        return registerer

    def as_factory(self) -> FactoryRegisterer[T]:
        """
        Continue the registration process of the service as a factory.
        """

        registerer = FactoryRegisterer[T](self._type_to_register, self._container)
        return registerer
