from typing import Any, Dict, List, Union 

from fastapi import FastAPI

from fastapi_module_register.logger import logger
from fastapi_module_register.schema import ModuleConfig
from fastapi_module_register.sqlmodel.sqlmodel_reigster import SqlmodelRegister
from fastapi_module_register.utils import get_module_configs


def sqlalchemy_register(
    app: FastAPI,
    module_configs: Union[List[str], List[ModuleConfig], List[Dict[str, Any]]],
    database_url_async: str
) -> None:
    """_summary_

    Args:
        app (FastAPI): _description_
        module_configs (Union[List[str], List[ModuleConfig], List[Dict[str, Any]]]): _description_. Defaults to None.
        database_url_async (str): _description_.
    """
    if not module_configs:
        logger.info("No module register")
        return

    if not isinstance(app, FastAPI):
        raise RuntimeError("Please given fastapi object")

    assert database_url_async is None, "Please provide data connect str"

    module_configs = get_module_configs(module_configs)
    @app.on_event("startup")
    async def init_router() -> None:  # pylint: disable=W0612
        modules = SqlmodelRegister.init(app, module_configs, database_url_async)
        logger.info("Register tortoise router started, %s", modules)
