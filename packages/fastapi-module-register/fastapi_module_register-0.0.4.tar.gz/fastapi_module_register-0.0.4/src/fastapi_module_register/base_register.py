from typing import Any, Dict, List, Callable, Optional, Type
import warnings

from fastapi import FastAPI, Depends

from fastapi_module_register.exceptions import ConfigurationError
from fastapi_module_register.interface.register_interface import RegisterInterface
from fastapi_module_register.schema import ModuleConfig
from fastapi_module_register.utils import import_string


class BaseRegister(RegisterInterface):

    @classmethod
    def init(cls, app: FastAPI, depend_func: List[Callable], module_configs: List[ModuleConfig]) -> None:
        if cls._inited or not module_configs:
            return

        cls.depend_func = [Depends(item) for item in depend_func if not callable(item)]
        cls.load_modules(module_configs)
        routers = cls.load_routers()
        cls.add_router(app, routers)

    @classmethod
    def load_modules(cls, module_configs: List[ModuleConfig]) -> None:
        """load modules

        Args:
            app (FastAPI): _description_
            modules (Optional[List[str]]): _description_
        """
        for module_config in module_configs:
            # Loading module
            module = cls._discover_model(module_config.module_path)
            if not module:
                continue
            module_config.module = module
            if not module_config.name:
                module_config.name = module.__name__
        cls.modules = {model.name: model for model in module_configs}

    @classmethod
    def _discover_model(cls, module_path: str, *args, **kwargs) -> Optional[Type["Any"]]:
        """_summary_

        Raises:
            ConfigurationError: _description_

        Returns:
            _type_: _description_
        """
        try:
            module = import_string(module_path)
        except ImportError:
            raise ConfigurationError(f'Module "{module_path}" not found')

        if cls._check_module(module):
            return module

    @classmethod
    def _discover_method(cls, module: Any, *args, **kwargs) -> Callable:
        raise NotImplementedError
    
    @classmethod
    def _check_module(cls, module: Any, *args, **kwargs) -> bool:
        raise NotImplementedError

    @classmethod
    def load_routers(cls) -> List[Any]:
        """load routers

        Returns:
            _type_: _description_
        """
        
        routers = []
        for _, module_config in cls.modules.items():
            if not cls._check_module(module_config.module):
                continue
            for config in module_config.router_config:
                method_func = cls._discover_method(module_config.module)
                exec_fun = getattr(method_func, config.method, None)
                if not exec_fun:
                    warnings.warn(f"Unsupported http method: {config.method}")
                    continue

                if config.method.lower() == "get":
                    filter_by_pk = True if '{pk}' in config.api_path else False
                    exec_fun_obj, res_schema = exec_fun(filter_by_pk)
                else:
                    exec_fun_obj, res_schema = exec_fun()

                if not callable(exec_fun_obj):
                    continue

                router = {
                    "path": config.api_path,
                    "endpoint": exec_fun_obj,
                    "methods": [config.method],
                    "response_model": res_schema
                }
                router.update(config.parameters)
                routers.append(router)
        return routers

    @classmethod
    def add_router(cls, app: FastAPI, routers: List[Dict]) -> None:
        """_summary_

        Args:
            app (FastAPI): _description_
            routers (List[Dict]): _description_
        """
        if not routers:
            return
        
        for router in routers:
            app.add_api_route(**router, dependencies=cls.depend_func)
