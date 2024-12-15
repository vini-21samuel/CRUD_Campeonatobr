from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Create (POST)
@router.post("/", response_model=schemas.PartidaResponse)
def criar_partida(partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    nova_partida = models.Partida(**partida.dict())
    db.add(nova_partida)
    db.commit()
    db.refresh(nova_partida)
    return nova_partida

# Read All (GET)
@router.get("/", response_model=List[schemas.PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return db.query(models.Partida).all()

# Read by ID (GET)
@router.get("/{partida_id}", response_model=schemas.PartidaResponse)
def buscar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    return partida

# Update (PUT)
@router.put("/{partida_id}", response_model=schemas.PartidaResponse)
def atualizar_partida(partida_id: int, partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    partida_atualizada = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida_atualizada:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    for key, value in partida.dict().items():
        setattr(partida_atualizada, key, value)
    db.commit()
    db.refresh(partida_atualizada)
    return partida_atualizada

# Delete (DELETE)
@router.delete("/{partida_id}", status_code=204)
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    db.delete(partida)
    db.commit()
