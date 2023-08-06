"""TODO
"""

from typing import Protocol, Sequence, TypeVar, runtime_checkable

from torch import nn

from torchlearn.training.results import Result

_T_co = TypeVar("_T_co", covariant=True)


@runtime_checkable
class Callback(Protocol[_T_co]):
    def __call__(self, module: nn.Module, epoch: int, results: Sequence[Result]) -> _T_co:
        raise NotImplementedError
