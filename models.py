from typing import Union
from uuid import UUID
from pydantic import BaseModel

class Produto(BaseModel):
    product_id: Union[UUID, None] = None
    name: str
    description: str
    price: float
