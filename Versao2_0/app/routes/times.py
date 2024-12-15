from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Create (POST)
@router.post("/", response_model=schemas.TimeResponse)
def criar_time(time: schemas.TimeCreate, db: Session = Depends(get_db)):
    novo_time = models.Time(**time.dict())
    db.add(novo_time)
    db.commit()
    db.refresh(novo_time)
    return novo_time

# Read All (GET)
@router.get("/", response_model=List[schemas.TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    return db.query(models.Time).all()

# Read by ID (GET)
@router.get("/{time_id}", response_model=schemas.TimeResponse)
def buscar_time(time_id: int, db: Session = Depends(get_db)):
    time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return time

# Update (PUT)
@router.put("/{time_id}", response_model=schemas.TimeResponse)
def atualizar_time(time_id: int, time: schemas.TimeCreate, db: Session = Depends(get_db)):
    time_atualizado = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not time_atualizado:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    for key, value in time.dict().items():
        setattr(time_atualizado, key, value)
    db.commit()
    db.refresh(time_atualizado)
    return time_atualizado

# Delete (DELETE)
@router.delete("/{time_id}", status_code=204)
def deletar_time(time_id: int, db: Session = Depends(get_db)):
    time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    db.delete(time)
    db.commit()
