from typing import List
import uuid
from fastapi import FastAPI
from models import Produto

app = FastAPI()

banco: List[Produto] = []

@app.get("/")
def root():
    return {"message": "root endpoint, please access other endpoints"}

@app.get("/produtos")
def get_products():
    return banco

@app.get("/produtos/{product_id}")
def get_product_by_id(product_id: str):
    for produto in banco:
        if produto.product_id == product_id:
            return produto.dict()

    return {"erro": "id não existe na base de dados"}

@app.post("/produtos")
def create_product(produto: Produto):
    produto.product_id = uuid.uuid4()
    banco.append(produto.dict())
    return produto.dict()