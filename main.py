from typing import List
import uuid
from fastapi import FastAPI, Path, Depends, HTTPException
from schemas import Produto, ProdutoCreate, Movimentacao, MovimentacaoCreate
from database.database import SessionLocal, engine
from sqlalchemy.orm import Session
from database import models, functions

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
* **Criar movimentações do inventário de produtos**
* **Consultar as movimentações já feitas**

"""

tags_metadata = [
  {
      "name": "Produtos",
      "description": "Operações com produtos"
  }
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
  title="API - MEGADADOS",
  description=description,
  openapi_tags = tags_metadata
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/produtos", tags=["Produtos"], summary="Chamada que devolve a lista de produtos no inventário", response_model=List[Produto])
def get_products(db: Session = Depends(get_db)):
  produtos = functions.get_produtos(db=db)
  return produtos

@app.get("/produtos/{product_id}", tags=["Produtos"], summary="Chamada que devolve um produto específico do inventário", response_model=Produto)
def get_product_by_id(product_id: str = Path(default=..., description="Id do Produto"), db: Session = Depends(get_db)):
  produto = functions.get_product_by_id(db=db, product_id=product_id)
  if produto is None:
    raise HTTPException(status_code=404, detail="usuário não encontrado")
  
  return produto

@app.post("/produtos", tags=["Produtos"], summary="Chamada para adicionar um produto ao inventário", response_model=Produto)
def create_product(produto_post: ProdutoCreate, db: Session = Depends(get_db)):
  produto = Produto()
  produto.product_id = uuid.uuid4()
  produto.name = produto_post.name
  produto.description = produto_post.description
  produto.price = produto_post.price
  produto.amount = produto_post.amount

  prod = functions.create_product(db=db, product=produto)
  if prod is None:
    raise HTTPException(status_code=400, detail="algo deu errado")

  return prod

@app.put("/produtos", tags=["Produtos"], summary="Chamada para alterar um produto do inventário", response_model=Produto)
def update_produto(produto: Produto, db: Session = Depends(get_db)):
  try:
    update = functions.update_product(db=db, product=produto)
    return update
  except:
    raise HTTPException(status_code=400, detail="produto não existe na base de dados")

@app.delete("/produtos/{product_id}", tags=["Produtos"], summary="Chamada para deletar um produto do inventário")
def delete_produto(product_id: str = Path(default=..., description="Id do Produto"), db: Session = Depends(get_db)):
  try:  
    delete = functions.delete_product(db=db, product_id=product_id)
    return delete
  except:
    raise HTTPException(status_code=400, detail="produto não existe na base de dados")

@app.get("/movimentacao",  tags=["Movimentações"], summary="Chamada que devolve a lista de modificações dos produtos", response_model=Movimentacao)
def get_movimentacao(db: Session = Depends(get_db)):
  movimentacoes = functions.get_movimentacao(db)
  return movimentacoes

@app.get("/movimentacao/{movimentacao_id}",  tags=["Movimentações"], summary="Chamada que devolve uma modificação específica", response_model=Movimentacao)
def get_movimentacao_by_id(movimentacao_id: str = Path(default=..., description="Id da movimentação"), db: Session = Depends(get_db)):
  movimentacao = functions.get_movimentacao_by_id(db=db, movimentacao_id=movimentacao_id)
  if movimentacao is None:
    raise HTTPException(status_code=404, detail="movimentação não encontrada")
  
  return movimentacao

@app.get("/movimentacao/produto/{product_id}",  tags=["Movimentações"],  summary="Chamada que devolve a lista de modificações de um produto específico", response_model=Movimentacao)
def get_movimentacao_by_product_id(product_id: str = Path(default=..., description="Id do produto"), db: Session = Depends(get_db)):
  movimentacao = functions.get_movimentacao_by_product_id(db=db, product_id=product_id)
  if movimentacao is None:
    raise HTTPException(status_code=404, detail="movimentação não encontrada")
  
  return movimentacao

@app.post("/movimentacao",  tags=["Movimentações"], summary="Chamada para adicionar uma movimentação a lista de movimentações", response_model=Movimentacao)
def create_movimentacao(movimentacao_post: MovimentacaoCreate, db: Session = Depends(get_db)):
  movi = Movimentacao()
  movi.movimentacao_id = uuid.uuid4()
  movi.product_id = movimentacao_post.product_id
  movi.amount = movimentacao_post.amount
  movi.operation = movimentacao_post.operation

  prod = functions.get_product_by_id(db=db, product_id=movimentacao_post.product_id)
  produto = Produto()
  produto.product_id = prod.product_id
  produto.name = prod.name
  produto.description = prod.description
  produto.price = prod.price

  if movimentacao_post.operation == "inserir":
    new_amount = prod.amount + movimentacao_post.amount
    produto.amount = new_amount
    prod = functions.update_product(db=db, product=produto)
  elif movimentacao_post.operation == "retirar":
    new_amount = prod.amount - movimentacao_post.amount
    produto.amount = new_amount
    prod = functions.update_product(db=db, product=produto)
  else:
    raise HTTPException(status_code=404, detail="operação inválida, utilize as operações 'retirar' ou 'inserir'")

  movimentacao = functions.create_movimentacao(db=db, movimentacao=movi)
  if movimentacao is None:
    raise HTTPException(status_code=404, detail="algo deu errado")
  
  return movimentacao