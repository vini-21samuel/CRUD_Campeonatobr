from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TimeResponse)
def criar_time(time: schemas.TimeCreate, db: Session = Depends(get_db)):
    db_time = models.Time(nome=time.nome, lugar=time.lugar)
    db.add(db_time)
    db.commit()
    db.refresh(db_time)
    return db_time

@router.get("/", response_model=List[schemas.TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    return db.query(models.Time).all()
