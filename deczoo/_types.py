import sys
from typing import Any, Callable, Protocol, Tuple, TypeVar, runtime_checkable

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

PS = ParamSpec("PS")
FuncReturnType = TypeVar("FuncReturnType", bound=Any)
FuncType = Callable[PS, FuncReturnType]

ReturnOnExceptionType = TypeVar("ReturnOnExceptionType", bound=Any)


@runtime_checkable
class SupportShape(Protocol):
    """
    Protocol for objects that have a shape attribute.
    In this context, a "dataframe"-like object.
    """

    @property
    def shape(self) -> Tuple[int, ...]:
        pass
