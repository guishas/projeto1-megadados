from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field

class Produto(BaseModel):
    product_id: Union[UUID, None] = Field(
        default="", title="Id do produto", example="7de18d3e-41f0-434e-8239-cf82970b1007"
    )  
    name: str = Field(
        default="", title="Nome do Produto", example="Refrigerante de Cola"
    )
    description: str = Field(
        default="", title="Descrição do produto", example="Lata de 350ml de refrigetante de cola"
    )
    price: float = Field(
        default=0.0, title="Preço do produto", example=4.90
    )
    amount: int = Field(default=0, title="Quantidade do produto", example=12
    )

class ProdutoPost(BaseModel):
    name: str = Field(
        default="", title="Nome do Produto", example="Refrigerante de Cola"
    )
    description: str = Field(
        default="", title="Descrição do produto", example="Lata de 350ml de refrigetante de cola"
    )
    price: float = Field(
        default=0.0, title="Preço do produto", example=4.90
    )
    amount: int = Field(default=0, title="Quantidade do produto", example=12
    )