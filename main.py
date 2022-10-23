from typing import List
import uuid
from fastapi import FastAPI, Query
from models import Produto

description = """
API desenvolvida para o projeto da disciplina de Megadados do Insper

## Desenvolvedores

* Guilherme Lunetta

* José Rafael Fernandes

## Funcionalidades

Ao utilizar essa API você pode:

* **Criar produtos**
* **Consultar o inventário de produtos**
* **Consultar um produto específico**
* **Alterar detalhes dos produtos**
* **Remover um produto específico**

"""

tags_metadata = [
    {
        "name": "Produtos",
        "description": "Operações com produtos"
    }
]

app = FastAPI(title="API - MEGADADOS",
    description=description,
    openapi_tags = tags_metadata
)

banco: List[Produto] = []

@app.get("/produtos", tags=["Produtos"], summary="Chamada que devolve a lista de produtos no inventário", response_model=Produto)
def get_products():
    return banco

@app.get("/produtos/{product_id}", tags=["Produtos"], summary="Chamada que devolve um produto específico do inventário", response_model=Produto)
def get_product_by_id(product_id: str = Query(default=..., description="Id do Produto")):
    for produto in banco:
      if str(produto["product_id"]) == product_id:
          return produto

    return {"erro": "produto não existe na base de dados"}

@app.post("/produtos", tags=["Produtos"], summary="Chamada para adicionar um produto ao inventário", response_model=Produto)
def create_product(produto: Produto):
    produto.product_id = uuid.uuid4()
    banco.append(produto.dict())
    return produto.dict()

@app.put("/produtos", tags=["Produtos"], summary="Chamada para alterar um produto do inventário")
def update_produto(produto: Produto):
  prod = None
  print(produto)
  for p in banco:
    if str(p["product_id"]) == str(produto.product_id):
      prod = produto

  if prod == None:
    return {"erro": "produto não existe na base de dados"}
  
  prod.name = produto.name
  prod.description = produto.description
  prod.price = produto.price
  prod.amount = produto.amount

  return prod.dict()

@app.delete("/produtos/{product_id}", tags=["Produtos"], summary="Chamada para deletar um produto do inventário")
def delete_produto(product_id: str = Query(default=..., description="Id do Produto")):
  for produto in banco:
    if str(produto["product_id"]) == product_id:
      banco.remove(produto)
      return {"message": "produto removido com sucesso"}

  return {"erro": "produto não existe na base de dados"}