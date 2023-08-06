from typing import Any, Dict, Type, TypeVar

from taipan_di.errors import TaipanUnregisteredError
from taipan_di.interfaces import BaseScope

__all__ = ["ServiceProvider"]

T = TypeVar("T")


class ServiceProvider:
    def __init__(self, services: Dict[Type[Any], BaseScope]) -> None:
        self._services = services.copy()

    def contains(self, type: Type[Any]) -> bool:
        return type in self._services

    def resolve(self, type: Type[T]) -> T:
        if not self.contains(type):
            raise TaipanUnregisteredError(f"Service {str(type)} is not registered")

        scope = self._services[type]
        result = scope.get_instance(self)

        return result
