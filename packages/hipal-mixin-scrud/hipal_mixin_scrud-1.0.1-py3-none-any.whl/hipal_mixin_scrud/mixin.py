from fastapi import Depends, Request
from typing import Any, List, Optional, Sequence, TypeVar
from typing import Type
from pydantic import BaseModel
from pydantic import create_model

from hipal_mixin_scrud.crud.generator import MixinGenerator
from hipal_mixin_scrud.crud.mixin_list import ListModelMixin
from hipal_mixin_scrud.schemas.paginate_params import PaginateParams

T = TypeVar("T", bound=BaseModel)
DEPENDENCIES = Optional[Sequence[Depends]]


class MixinCrud(MixinGenerator, ListModelMixin):
    """
    Mixin crud.
    """

    def __init__(
        self,
        model,
        db_session,
        schema: Type[T],
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None,
        create_schema: Optional[BaseModel] = None,
        update_schema: Optional[BaseModel] = None,
        has_get_list: bool = True,
        has_update: bool = True,
        has_create: bool = True,
        has_get_one: bool = True,
        has_delete_one: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            model=model,
            db_session=db_session,
            schema=schema,
            prefix=prefix,
            tags=tags,
            create_schema=create_schema,
            update_schema=update_schema,
            has_get_list=has_get_list,
            has_update=has_update,
            has_create=has_create,
            has_get_one=has_get_one,
            has_delete_one=has_delete_one,
            **kwargs,
        )

    def _get_paginate(self, *args: Any, **kwargs: Any):
        def route(
            request: Request,
            paginate_params: PaginateParams = Depends(),
        ):
            path = request.url._url.split("?")[0]
            return self.paginate(
                db_session=self.db_session,
                model=self.model,
                paginate_params=paginate_params,
                squema=self.schema,
                path=path,
            )

        return route

    def _get_one(self, *args: Any, **kwargs: Any):
        def route(item_id):
            item = (
                self.db_session.query(self.model)
                .filter(getattr(self.model, self._pk) == item_id)
                .first()
            )

            return item

        return route

    def _create(self, *args: Any, **kwargs: Any):
        def route(model: self.create_schema):
            db_model = self.model(**model.dict())
            self.db_session.add(db_model)
            self.db_session.commit()
            self.db_session.refresh(db_model)
            return db_model

        return route

    def _update(self, *args: Any, **kwargs: Any):
        def route(
            item_id,
            model: self.update_schema,
        ):
            db_model = self._get_one()(item_id)

            for key, value in model.dict(exclude={self._pk}).items():
                if hasattr(db_model, key):
                    setattr(db_model, key, value)

            self.db_session.commit()
            self.db_session.refresh(db_model)
            return db_model

        return route

    def _delete_one(self, *args: Any, **kwargs: Any):
        def route(item_id):
            db_model = self._get_one(item_id)
            self.db_session.delete(db_model)
            return {"msg": "Eliminado"}

        return route
