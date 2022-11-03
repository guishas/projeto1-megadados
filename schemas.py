from typing import Union
from uuid import UUID
from pydantic import BaseModel, Field

class ProdutoBase(BaseModel): 
  name: str = Field(
      default="", title="Nome do Produto", example="Refrigerante de Cola"
  )
  description: str = Field(
      default="", title="Descrição do produto", example="Lata de 350ml de refrigerante de cola"
  )
  price: float = Field(
      default=0.0, title="Preço do produto", example=4.90
  )
  amount: int = Field(
    default=0, title="Quantidade do produto", example=12
  )

class ProdutoCreate(ProdutoBase):
  name: str = Field(
      default="", title="Nome do Produto", example="Refrigerante de Cola"
  )
  description: str = Field(
      default="", title="Descrição do produto", example="Lata de 350ml de refrigerante de cola"
  )
  price: float = Field(
      default=0.0, title="Preço do produto", example=4.90
  )
  amount: int = Field(
    default=0, title="Quantidade do produto", example=12
  )

class Produto(ProdutoBase):
  product_id: Union[UUID, None] = Field(
      default="", title="Id do produto", example="7de18d3e-41f0-434e-8239-cf82970b1007"
  ) 
  
  class Config:
    orm_mode=True

class MovimentacaoBase(BaseModel):
  product_id: str = Field(
    default=""
  )
  amount: int = Field(
    default=0
  )
  operation: str = Field(
    default=""
  )

class MovimentacaoCreate(MovimentacaoBase):
  product_id: str = Field(
    default=""
  )
  amount: int = Field(
    default=0
  )
  operation: str = Field(
    default=""
  )

class Movimentacao(MovimentacaoBase):
  movimentacao_id: str = Field(
    default=""
  )

  class Config:
    orm_mode=True