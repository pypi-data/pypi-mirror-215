from abc import abstractmethod, ABC
from typing import Union, Dict, List, Any

from fastapi import FastAPI

from fastapi_module_register.schema import ModuleConfig


class RegisterInterface(ABC):

    modules: Dict[str, ModuleConfig] = {}
    _inited: bool = False

    @classmethod
    @abstractmethod
    def init(cls, app: FastAPI, module_configs: List[ModuleConfig], *args, **kwargs) -> None:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load_modules(cls, module_dirs: List[str], *args, **kwargs) -> None:
        raise NotImplementedError
    
    @classmethod
    @abstractmethod
    def load_routers(cls) -> List[Any]:
        raise NotImplementedError
