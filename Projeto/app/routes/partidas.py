from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from app.services.partidas_service import PartidaService
from app.schemas.partida import PartidaCreate, PartidaResponse
from database.database import SessionLocal
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PartidaResponse)
def criar_partida(partida: PartidaCreate, db: Session = Depends(get_db)):
    return PartidaService.criar_partida(db, partida)

@router.get("/", response_model=List[PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    return PartidaService.listar_partidas(db)

@router.get("/{partida_id}", response_model=PartidaResponse)
def obter_partida(partida_id: int, db: Session = Depends(get_db)):
    return PartidaService.obter_partida(db, partida_id)

from app.schemas.partida import PartidaUpdate  # você vai precisar criar esse schema também

@router.put("/{partida_id}", response_model=PartidaResponse)
def atualizar_partida(partida_id: int, partida: PartidaUpdate, db: Session = Depends(get_db)):
    return PartidaService.atualizar_partida(db, partida_id, partida)


@router.delete("/{partida_id}")
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    PartidaService.deletar_partida(db, partida_id)
    return {"detail": "Partida deletada com sucesso"}
