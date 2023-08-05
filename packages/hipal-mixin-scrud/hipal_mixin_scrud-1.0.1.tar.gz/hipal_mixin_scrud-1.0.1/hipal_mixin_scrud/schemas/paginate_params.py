from typing import Optional
from pydantic import BaseModel

from hipal_mixin_scrud.enums.operators import Operators
from hipal_mixin_scrud.enums.sorts import Sort


class PaginateParams(BaseModel):
    offset: Optional[int] = 0
    limit: Optional[int] = 10
    search_field: Optional[str]
    search_value: Optional[str] = ""
    sort: Optional[Sort]
    sort_field: Optional[str]
