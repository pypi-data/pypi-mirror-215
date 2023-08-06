from typing import Any, Type, Tuple, Optional, Callable

from sqlmodel import SQLModel

from fastapi_module_register.interface.method_interface import MethodInterface
from fastapi_module_register.schema import BaseApiOut


class SqlmodelMethod(MethodInterface):

    def __init__(self, module: Type[SQLModel], async_session, depend_func: Optional[Callable] = None) -> None:
        """_summary_

        Args:
            module (Model): The tortoise model
            depend_func (Optional[Callable], optional): _description_. Defaults to None.
        """
        self._module = module
        self._depend_func = depend_func
        self._base_request = pydantic_model_creator(
            module,
            name=f"{module.__name__}_req",
            exclude=(module._meta.pk_attr, )
        )
        self._get_response = pydantic_model_creator(module, name=f"{module.__name__}_get")
        self._base_response = pydantic_model_creator(module, name=f"{module.__name__}_res")

    def get(self,  filter_by_pk: bool = False, *args, **kwargs) -> Tuple[Callable, Any]:
        return None, None
    
    def post(self, *args, **kwargs) -> Tuple[Callable, Any]:
        return None, None
    
    def put(self, *args, **kwargs) -> Tuple[Callable, Any]:
        return None, None
    
    def delete(self, *args, **kwargs) -> Tuple[Callable, Any]:
        return None, None