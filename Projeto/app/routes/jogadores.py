from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import SessionLocal, get_db
from app.services.jogadores_service import JogadorService
from app.schemas.jogador import JogadorCreate, JogadorResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JogadorResponse)
def criar_jogador(jogador: JogadorCreate, db: Session = Depends(get_db)):
    return JogadorService.criar_jogador(db, jogador)

@router.get("/", response_model=List[JogadorResponse])
def listar_jogadores(db: Session = Depends(get_db)):
    return JogadorService.listar_jogadores(db)

@router.get("/{jogador_id}", response_model=JogadorResponse)
def obter_jogador(jogador_id: int, db: Session = Depends(get_db)):
    return JogadorService.obter_jogador(db, jogador_id)

@router.put("/{jogador_id}", response_model=JogadorResponse)
def atualizar_jogador(jogador_id: int, jogador: JogadorCreate, db: Session = Depends(get_db)):
    return JogadorService.atualizar_jogador(db, jogador_id, jogador)

@router.delete("/{jogador_id}")
def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    JogadorService.deletar_jogador(db, jogador_id)
    return {"detail": "Jogador deletado com sucesso"}
