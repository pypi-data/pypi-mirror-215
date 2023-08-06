from typing import Optional, Callable, Type, Tuple, Union

from fastapi import Depends, HTTPException
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate
from tortoise.models import Model
from tortoise.contrib.pydantic.base import PydanticModel
from tortoise.contrib.pydantic.creator import pydantic_model_creator

from fastapi_module_register.interface.method_interface import MethodInterface
from fastapi_module_register.schema import BaseApiOut


class TortoiseMethod(MethodInterface):

    def __init__(self, module: Type[Model])-> None:
        """_summary_

        Args:
            module (Model): The tortoise model
        """
        self._module = module
        self._base_request = pydantic_model_creator(
            module,
            name=f"{module.__name__}_request",
            exclude=(module._meta.pk_attr, ),
            exclude_readonly=True
        )
        self._get_response = pydantic_model_creator(module, name=f"{module.__name__}_get")
        self._base_response = pydantic_model_creator(module, name=f"{module.__name__}_response")

    def get(self, filter_by_pk: bool = False, *args, **kwargs) -> Tuple[Callable, Union[Type[PydanticModel], Type[Page[PydanticModel]]]]:
        """The http get method
        Args:
            filter_by_pk (bool): Get item by pk
        Returns:
            Callable: _description_
        """
        if filter_by_pk:
            async def wapper(pk: int): # type: ignore
                result = self._module.get(pk=pk)
                result = await self._get_response.from_queryset_single(result)
                return result
            return wapper, self._base_response
        async def wapper(params: Params = Depends()):
            results = self._module.filter()
            results = await paginate(results, params)
            return results
        return wapper, Page[self._get_response]

    def post(
        self,
        request_model: Optional[Type[PydanticModel]] = None,
    ) -> Tuple[Callable, Type[PydanticModel]]:
        """The http post method

        Args:
            request_model (Optional[Type[PydanticModel]], optional): _description_. Defaults to None.

        Returns:
            Callable: _description_
        """
        if not request_model:
            request_model = self._base_request

        async def wapper(req: request_model): # type: ignore
            save_item = await self._module.create(**req.dict(exclude_unset=True))
            return await self._base_response.from_tortoise_orm(save_item)
        return wapper, self._base_response

    def put(
        self,
        request_model: Optional[Type[PydanticModel]] = None
    ) -> Tuple[Callable, Type[PydanticModel]]:
        """_summary_

        Args:
            request_model (Optional[Type[PydanticModel]], optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if not request_model:
            request_model = self._base_request

        async def wapper(pk: int, req: request_model): # type: ignore
            await self._module.filter(pk=pk).update(**req.dict(exclude_unset=True))
            return await self._base_response.from_queryset_single(
                self._module.get(pk=pk)
            )
        return wapper, self._base_response

    def delete(self) -> Tuple[Callable, Type[BaseApiOut]]:
        """Delete the item by primary key

        Returns:
            Callable: _description_
        """
        async def wapper(pk: int):
            item = await self._module.get(pk=pk)
            if not item:
                raise HTTPException(status_code=404, detail=f"{self._module.__name__} {pk} not found")
            await item.delete()
            return BaseApiOut()

        return wapper, BaseApiOut
