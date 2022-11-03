from typing import List
import uuid
from fastapi import FastAPI, Path, Depends, HTTPException
from schemas import Produto, ProdutoCreate
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

# banco: List[Produto] = []

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