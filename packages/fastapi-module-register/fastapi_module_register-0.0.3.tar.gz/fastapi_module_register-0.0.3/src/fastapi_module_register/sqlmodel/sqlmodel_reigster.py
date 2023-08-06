from typing import Any, List, Optional, Type

from fastapi import FastAPI
from sqlmodel import SQLModel

from fastapi_module_register.base_register import BaseRegister
from fastapi_module_register.schema import ModuleConfig
from fastapi_module_register.sqlmodel.sqlmodel_method import SqlmodelMethod
from fastapi_module_register.sqlmodel.utils import AsyncSession


class SqlmodelRegister(BaseRegister):

    @classmethod
    def init(cls, app: FastAPI, module_configs: List[ModuleConfig], database_async_url: str) -> None:
        """_summary_

        Args:
            app (FastAPI): _description_
            module_configs (List[ModuleConfig]): _description_
            database_async_url (str): _description_
        """
        cls.init(app, module_configs)
        cls.async_session = AsyncSession.init(database_async_url)

    @classmethod
    def _discover_method(cls, module: Type[Any]) -> Optional[SqlmodelMethod]:
        """_summary_

        Args:
            module (Type[Any]): _description_

        Returns:
            Optional[SqlmodelMethod]: _description_
        """
        if cls._check_module(module):
            return SqlmodelMethod(module, AsyncSession.gen_session)

    @classmethod
    def _check_module(cls, module: Any, *args, **kwargs) -> bool:
        """_summary_

        Args:
            module (Any): _description_

        Returns:
            bool: _description_
        """
        if not module:
            return False

        if issubclass(module, SQLModel) and module.Config.__table__:
            return True
