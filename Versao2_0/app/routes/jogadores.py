from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Create (POST)
@router.post("/", response_model=schemas.JogadorResponse)
def criar_jogador(jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    novo_jogador = models.Jogador(**jogador.dict())
    db.add(novo_jogador)
    db.commit()
    db.refresh(novo_jogador)
    return novo_jogador

# Read All (GET)
@router.get("/", response_model=List[schemas.JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    return db.query(models.Jogador).all()

# Read by ID (GET)
@router.get("/{jogador_id}", response_model=schemas.JogadorResponse)
def buscar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    return jogador

# Update (PUT)
@router.put("/{jogador_id}", response_model=schemas.JogadorResponse)
def atualizar_jogador(jogador_id: int, jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    jogador_atualizado = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador_atualizado:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    for key, value in jogador.dict().items():
        setattr(jogador_atualizado, key, value)
    db.commit()
    db.refresh(jogador_atualizado)
    return jogador_atualizado

# Delete (DELETE)
@router.delete("/{jogador_id}", status_code=204)
def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    db.delete(jogador)
    db.commit()
