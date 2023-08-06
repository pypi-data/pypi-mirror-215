from typing import Any, Optional, Type

from tortoise.models import Model

from fastapi_module_register.base_register import BaseRegister
from fastapi_module_register.tortoise.tortoise_method import TortoiseMethod


class TortoiseRegister(BaseRegister):

    @classmethod
    def _discover_method(cls, module: Type[Model]) -> Optional[TortoiseMethod]:
        """
        """
        if cls._check_module(module):
            return TortoiseMethod(module)

    @classmethod
    def _check_module(cls, module: Any, *args, **kwargs) -> bool:
        if issubclass(module, Model) and not module._meta.abstract and module._meta.app:
            return True
        return False
