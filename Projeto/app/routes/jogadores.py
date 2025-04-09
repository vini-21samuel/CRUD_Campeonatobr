from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, get_db
from app.services.jogadores_service import JogadorService
from app.schemas.jogador import JogadorCreate, JogadorResponse
from app.models.jogador import Jogador
from app.models.time import Time
import logging

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@router.get("/torneio/{torneio_id}", response_model=List[JogadorResponse])
def listar_jogadores_por_torneio(torneio_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Buscando jogadores para o torneio ID: {torneio_id}")
        jogadores = (
            db.query(Jogador)
            .join(Time, Jogador.time_id == Time.id, isouter=True)
            .filter(Time.torneio_id == torneio_id)
            .all()
        )
        logger.info(f"Jogadores encontrados: {len(jogadores)}")
        return [
            {
                "id": j.id,
                "nome": j.nome,
                "posicao": j.posicao,
                "gols": j.gols if j.gols is not None else 0,
                "time_id": j.time_id,
                "time": {
                    "id": j.time.id,
                    "nome": j.time.nome,
                    "lugar": j.time.lugar if j.time and hasattr(j.time, 'lugar') else None
                } if j.time else None
            }
            for j in jogadores
        ] if jogadores else []
    except Exception as e:
        logger.error(f"Erro ao listar jogadores para torneio {torneio_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erro interno ao buscar jogadores: {str(e)}")