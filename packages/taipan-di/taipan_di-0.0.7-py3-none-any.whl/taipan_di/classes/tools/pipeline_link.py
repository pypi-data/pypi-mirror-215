from __future__ import annotations

import abc
from typing import Callable, Generic, Optional, TypeVar

__all__ = ["PipelineLink"]

T = TypeVar("T")
U = TypeVar("U")


class PipelineLink(Generic[T, U], metaclass=abc.ABCMeta):
    """
    A component of a pipeline.

    When writing your own links, you only have to write the `_handle` method.
    """

    def __init__(self) -> None:
        self._next = None

    def _set_next(self, next: PipelineLink[T, U]) -> PipelineLink[T, U]:
        self._next = next
        return self._next

    def exec(self, request: T) -> Optional[U]:
        """
        Execute the pipeline that starts at this link.
        """

        next_function = self._next.exec if self._next is not None else lambda req: None

        return self._handle(request, next_function)

    @abc.abstractmethod
    def _handle(self, request: T, next: Callable[[T], Optional[U]]) -> Optional[U]:
        return next(request)
