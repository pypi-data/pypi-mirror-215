from typing import Any, Dict, Type, cast, TypeVar

from taipan_di.interfaces import BaseServiceProvider, BaseScope

from .service_provider import ServiceProvider

__all__ = ["ServiceContainer"]

T = TypeVar("T")


class ServiceContainer:
    def __init__(self) -> None:
        self._services = cast(Dict[Type[Any], BaseScope], {})

    def contains(self, type: Type[Any]) -> bool:
        return type in self._services

    def register(self, type: Type[T], service: BaseScope[T]) -> None:
        self._services[type] = service

    def build(self) -> BaseServiceProvider:
        provider = ServiceProvider(self._services)
        return provider
