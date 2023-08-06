from abc import abstractmethod, ABC
from typing import Any, Callable, Optional, Tuple


class MethodInterface(ABC):

    @abstractmethod
    def get(self, *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError

    @abstractmethod
    def post(self, *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError

    @abstractmethod
    def put(self, *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, *args, **kwars) -> Optional[Tuple[Callable, Any]]:
        raise NotImplementedError
