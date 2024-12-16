# app/routes/jogadores.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter()

# Read All (GET) - Listar jogadores com o time
@router.get("/", response_model=List[schemas.JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    try:
        return db.query(models.Jogador).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Erro ao listar jogadores: {str(e)}")

#Criar jogador
@router.post("/", response_model=schemas.JogadorResponse)
def criar_jogador(jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    try:
        novo_jogador = models.Jogador(
            nome=jogador.nome,
            posicao=jogador.posicao,
            gols=jogador.gols,
            time_id=jogador.time_id
        )
        db.add(novo_jogador)
        db.commit()
        db.refresh(novo_jogador)
        return novo_jogador
    except Exception as e:
        db.rollback()  # Reverte a transação em caso de erro
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                             detail=f"Erro ao criar jogador: {str(e)}")

# Update (PUT) - Atualizar jogador
@router.put("/{jogador_id}", response_model=schemas.JogadorResponse)
def atualizar_jogador(jogador_id: int, jogador: schemas.JogadorCreate, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    
    if not db_jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    db_jogador.nome = jogador.nome
    db_jogador.posicao = jogador.posicao
    db_jogador.gols = jogador.gols
    db_jogador.time_id = jogador.time_id
    db.commit()
    db.refresh(db_jogador)
    
    return db_jogador

# Delete (DELETE) - Excluir jogador
@router.delete("/{jogador_id}", response_model=schemas.JogadorResponse)
def excluir_jogador(jogador_id: int, db: Session = Depends(get_db)):
    db_jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()

    if not db_jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    db.delete(db_jogador)
    db.commit()
    
    return db_jogador
