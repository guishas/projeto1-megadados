from typing import List
import uuid
from fastapi import FastAPI
from models import Produto

app = FastAPI()

banco: List[Produto] = []

@app.get("/produtos")
def get_products():
    return banco

@app.get("/produtos/{product_id}")
def get_product_by_id(product_id: str):
    for produto in banco:
      if str(produto["product_id"]) == product_id:
          return produto

    return {"erro": "produto não existe na base de dados"}

@app.post("/produtos")
def create_product(produto: Produto):
    produto.product_id = uuid.uuid4()
    banco.append(produto.dict())
    return produto.dict()

@app.put("/produtos")
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

  return prod.dict()

@app.delete("/produtos/{product_id}")
def delete_produto(product_id: str):
  for produto in banco:
    if str(produto["product_id"]) == product_id:
      banco.remove(produto)
      return {"message": "produto removido com sucesso"}

  return {"erro": "produto não existe na base de dados"}