from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user_db = 'postgres'
pwd_db = '123789123'

SQLALCHEMY_DATABASE_URL = f"postgresql://{user_db}:{pwd_db}@localhost/teste_pontotel"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()