from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv('USER_DB')
PASSWORD = os.getenv('PASSWORD')
MY_SQL_SERVER = os.getenv('MY_SQL_SERVER')
DB = os.getenv('DB')

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{MY_SQL_SERVER}/{DB}"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()