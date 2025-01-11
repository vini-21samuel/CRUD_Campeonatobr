# app/routes/times.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Read All (GET) - Listar times com jogadores
@router.get("/", response_model=List[schemas.TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    try:
        return db.query(models.Time).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Erro ao listar times: {str(e)}")

# Create (POST) - Criar time
@router.post("/", response_model=schemas.TimeResponse)
def criar_time(time: schemas.TimeCreate, db: Session = Depends(get_db)):
    try:
        novo_time = models.Time(nome=time.nome, lugar=time.lugar)
        db.add(novo_time)
        db.commit()
        db.refresh(novo_time)
        return novo_time
    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Erro ao criar time: {str(e)}")

# Update (PUT) - Atualizar time
@router.put("/{time_id}", response_model=schemas.TimeResponse)
def atualizar_time(time_id: int, time: schemas.TimeCreate, db: Session = Depends(get_db)):
    db_time = db.query(models.Time).filter(models.Time.id == time_id).first()
    
    if not db_time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    db_time.nome = time.nome
    db_time.lugar = time.lugar
    db.commit()
    db.refresh(db_time)
    
    return db_time

# Excluir time
@router.delete("/{time_id}", response_model=schemas.TimeResponse)
def excluir_time(time_id: int, db: Session = Depends(get_db)):
    try:
        db_time = db.query(models.Time).filter(models.Time.id == time_id).first()

        if not db_time:
            raise HTTPException(status_code=404, detail="Time não encontrado")

        # Atualizar as partidas envolvendo o time
        db.query(models.Partida).filter(
            (models.Partida.time1_id == time_id) | (models.Partida.time2_id == time_id)
        ).update({models.Partida.time1_id: None, models.Partida.time2_id: None}, synchronize_session=False)
        
        # Excluir o time
        db.delete(db_time)
        db.commit()
        
        return db_time
    except Exception as e:
        db.rollback()  # Reverte qualquer transação aberta em caso de erro
        raise HTTPException(status_code=500, detail=f"Erro ao excluir time: {str(e)}")
