from sqlalchemy.orm import Session
from . import models
import schemas

def get_produtos(db: Session, limit: int = None):
  if limit == None:
    return db.query(models.Produto).all()
  else:
    return db.query(models.Produto).limit(limit).all()

def get_product_by_id(db: Session, product_id: str):
  return db.query(models.Produto).filter(models.Produto.productId == product_id).first()

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
