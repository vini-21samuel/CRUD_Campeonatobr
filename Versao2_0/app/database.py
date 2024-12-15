# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

DATABASE_URL = "postgresql://vini_samuel:210503@localhost:5432/interclasse_db"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True para logs de execução

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
