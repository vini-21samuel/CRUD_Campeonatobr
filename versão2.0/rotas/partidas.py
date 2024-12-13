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

@router.post("/", response_model=schemas.PartidaResponse)
def criar_partida(partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    db_partida = models.Partida(**partida.dict())
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida

@router.get("/", response_model=List[schemas.PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return db.query(models.Partida).all()
