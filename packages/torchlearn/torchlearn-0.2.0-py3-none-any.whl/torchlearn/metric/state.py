"""TODO metric_state docstring
"""
from abc import ABC, abstractmethod
from inspect import Signature, signature
from typing import Any, Mapping, Optional, Sequence, Union

import torch


class State(ABC):
    """TODO MetricState docstring"""

    _parameters: Sequence[str]

    def __init__(self, parameters: Optional[Sequence[str]] = None) -> None:
        sig = self.signature()
        if parameters is None:
            parameters = list(sig.parameters)

        if len(parameters) != len(sig.parameters):
            raise ValueError(
                f"State expects {len(sig.parameters)} parameters ({sig.parameters}),"
                f"but {len(parameters)} parameters were given ({parameters})."
            )

        self._parameters = tuple(parameters)

    @torch.no_grad()
    def __call__(self, kwargs: Mapping[str, Any]) -> Any:
        kwargs = {name: kwargs[name] for name in self.parameters if name in kwargs}
        return self.update(**kwargs)

    @property
    def parameters(self) -> Sequence[str]:
        return self._parameters

    @abstractmethod
    def reset(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def compute(*args: Any, **kwargs: Any) -> Any:
        pass

    def process(self, outputs: Union[Sequence[Any], Mapping[str, Any]]) -> Any:
        if isinstance(outputs, Mapping):
            try:
                outputs = tuple(outputs[a] for a in self._parameters)
            except KeyError as exception:
                key = exception.args[0]
                raise ValueError(
                    f"Missing key from output: expected '{key}' to be present, but only found {tuple(outputs)}."
                ) from exception
        if len(outputs) != len(self._parameters):
            raise ValueError(
                f"Argument mismatch: expected {len(self._parameters)} " f"arguments, but got {len(outputs)} arguments."
            )
        return self.update(*outputs)

    def signature(self) -> Signature:
        return signature(self.update)
