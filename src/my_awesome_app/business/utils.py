from typing import Generic, TypeVar

from pydantic.generics import GenericModel

T = TypeVar('T')


class GenericPage(GenericModel, Generic[T]):
    data: list[T]
    total_items: int
