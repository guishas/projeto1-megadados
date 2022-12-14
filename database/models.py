from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database.database import Base

class Produto(Base):
  __tablename__ = "produtos"

  product_id = Column(String(255), primary_key=True, index=True)
  name = Column(String(255))
  description = Column(String(255))
  price = Column(Float)
  amount = Column(Integer)

class Movimentacao(Base):
  __tablename__ = "movimentacao"

  movimentacao_id = Column(String(255), primary_key=True, index=True)
  product_id = Column(String(255))
  amount = Column(Integer)
  operation = Column(String(255))