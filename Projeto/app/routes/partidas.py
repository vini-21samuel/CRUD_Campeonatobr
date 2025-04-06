from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.services.partidas_service import PartidaService
from app.schemas.partida import PartidaCreate, PartidaResponse, PartidaUpdate
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/", response_model=PartidaResponse)
def criar_partida(partida: PartidaCreate, db: Session = Depends(get_db)):
    return PartidaService.criar_partida(db, partida)

@router.get("/", response_model=List[PartidaResponse])
def listar_partidas(torneio_id: Optional[int] = None, db: Session = Depends(get_db)):
    return PartidaService.listar_partidas(db, torneio_id)

@router.get("/{partida_id}", response_model=PartidaResponse)
def obter_partida(partida_id: int, db: Session = Depends(get_db)):
    return PartidaService.obter_partida(db, partida_id)

@router.put("/{partida_id}", response_model=PartidaResponse)
def atualizar_partida(partida_id: int, partida: PartidaUpdate, db: Session = Depends(get_db)):
    return PartidaService.atualizar_partida(db, partida_id, partida)

@router.delete("/{partida_id}")
def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    PartidaService.deletar_partida(db, partida_id)
    return {"detail": "Partida deletada com sucesso"}