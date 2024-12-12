from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Jogador
from schemas import JogadorCreate, JogadorResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JogadorResponse, tags=["Jogadores"])
def criar_jogador(jogador: JogadorCreate, db: Session = Depends(get_db)):
    novo_jogador = Jogador(
        nome=jogador.nome,
        posicao=jogador.posicao,
        time_id=jogador.time_id,
        gols=jogador.gols
    )
    db.add(novo_jogador)
    db.commit()
    db.refresh(novo_jogador)
    return novo_jogador
