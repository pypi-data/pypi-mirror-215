from __future__ import annotations
from typing import Generic, List, Type, TypeVar

from taipan_di.errors import TaipanRegistrationError
from taipan_di.interfaces import BaseServiceProvider, BaseServiceContainer

from taipan_di.classes.scopes import FactoryScope, SingletonScope
from taipan_di.classes.tools import PipelineLink, PipelineFactory, instanciate_service

__all__ = ["PipelineRegisterer"]

T = TypeVar("T")
U = TypeVar("U")


class PipelineRegisterer(Generic[T, U]):
    """
    Part of the registration process.

    You shouldn't have to create instances of this class by yourself.
    """

    def __init__(
        self,
        type_to_register: Type[PipelineLink[T, U]],
        container: BaseServiceContainer,
    ) -> None:
        self._type_to_register = type_to_register
        self._container = container
        self._link_types: List[Type[PipelineLink[T, U]]] = []

    def add(self, link: Type[PipelineLink[T, U]]) -> PipelineRegisterer[T, U]:
        """
        Add a link to the pipeline you are building.

        Returns itself, so that you can chain `add` calls.
        """

        self._link_types.append(link)
        return self

    def as_singleton(self) -> None:
        """
        Register the pipeline built as a singleton.

        Will throw an error if the pipeline is empty.
        """

        self._register(True)

    def as_factory(self) -> None:
        """
        Register the pipeline built as a factory.

        Will throw an error if the pipeline is empty.
        """

        self._register(False)

    def _register(self, as_singleton: bool) -> None:
        if len(self._link_types) == 0:
            raise TaipanRegistrationError(
                f"Pipeline[{str(T)}, {str(U)}] is empty ! Add at least one link"
            )

        def create_pipeline(provider: BaseServiceProvider) -> PipelineLink[T, U]:
            factory = PipelineFactory[T, U]()

            for link_type in self._link_types:
                link = instanciate_service.instanciate_service(link_type, provider)
                factory.add(link)

            return factory.build()

        if as_singleton:
            scope = SingletonScope[PipelineLink[T, U]](create_pipeline)
        else:
            scope = FactoryScope[PipelineLink[T, U]](create_pipeline)

        self._container.register(self._type_to_register, scope)
