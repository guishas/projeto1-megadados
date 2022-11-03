from sqlalchemy.orm import Session
from . import models
import schemas

def get_produtos(db: Session, limit: int = None):
  if limit == None:
    return db.query(models.Produto).all()
  else:
    return db.query(models.Produto).limit(limit).all()

def get_product_by_id(db: Session, product_id: str):
  return db.query(models.Produto).filter(models.Produto.product_id == product_id).first()

def create_product(db: Session, product: schemas.Produto):
  db_product = models.Produto(
    product_id = str(product.product_id),
    name = product.name,
    description = product.description,
    price = product.price,
    amount = product.amount
  )

  db.add(db_product)
  db.commit()
  db.refresh(db_product)
  return db_product

def update_product(db: Session, product: schemas.Produto):
  print(product.amount)
  db.query(models.Produto).filter(models.Produto.product_id == product.product_id).update({
    'name': product.name,
    'description': product.description,
    'price': product.price,
    'amount': product.amount
  })
  print(product.product_id)
  db.commit()
  return product

def delete_product(db: Session, product_id: str):
  db.query(models.Produto).filter(models.Produto.product_id == product_id).delete()
  db.commit()  
  return {"message": "produto removido com sucesso"}

def create_movimentacao(db: Session, movimentacao: schemas.Movimentacao):
  db_movimentacao = models.Movimentacao(
    movimentacao_id = movimentacao.movimentacao_id,
    product_id = movimentacao.product_id,
    amount = movimentacao.amount,
    operation = movimentacao.operation
  )

  db.add(db_movimentacao)
  db.commit()
  db.refresh(db_movimentacao)
  return db_movimentacao

def get_movimentacao(db: Session):
  return db.query(models.Movimentacao).all()

def get_movimentacao_by_id(db: Session, movimentacao_id: str):
  return db.query(models.Movimentacao).filter(models.Movimentacao.movimentacao_id == movimentacao_id).first()

def get_movimentacao_by_product_id(db: Session, product_id: str):
  print("functions")
  return db.query(models.Movimentacao).filter(models.Movimentacao.product_id == product_id).all()