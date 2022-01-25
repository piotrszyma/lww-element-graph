from typing import Protocol, Any, Union


class SupportsDunderLT(Protocol):
    def __lt__(self, __other: Any) -> Any:
        ...


class SupportsDunderGT(Protocol):
    def __gt__(self, __other: Any) -> Any:
        ...


SupportsRichComparison = Union[SupportsDunderLT, SupportsDunderGT]
