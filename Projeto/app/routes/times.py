from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.services.times_service import TimeService
from app.schemas.time import TimeCreate, TimeResponse
from app.database.database import SessionLocal
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

@router.post("/", response_model=TimeResponse)
def criar_time(
    nome: str = Form(...),
    lugar: str = Form(...),
    torneio_id: int = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    time_data = TimeCreate(nome=nome, lugar=lugar, torneio_id=torneio_id)
    return TimeService.criar_time(db, time_data, logo)

@router.get("/", response_model=List[TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    return TimeService.listar_times(db)

@router.get("/torneio/{torneio_id}", response_model=List[TimeResponse])
def listar_times_por_torneio(torneio_id: int, db: Session = Depends(get_db)):
    return TimeService.listar_times_por_torneio(db, torneio_id)

@router.get("/{time_id}", response_model=TimeResponse)
def obter_time(time_id: int, db: Session = Depends(get_db)):
    return TimeService.obter_time(db, time_id)

@router.put("/{time_id}", response_model=TimeResponse)
def atualizar_time(
    time_id: int,
    nome: str = Form(...),
    lugar: str = Form(...),
    torneio_id: int = Form(...),
    logo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    time_data = TimeCreate(nome=nome, lugar=lugar, torneio_id=torneio_id)
    return TimeService.atualizar_time(db, time_id, time_data, logo)

@router.delete("/{time_id}", status_code=204)
def deletar_time(time_id: int, db: Session = Depends(get_db)):
    try:
        resultado = TimeService.deletar_time(db, time_id)
        if not resultado:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return None  # Status 204 não retorna corpo
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Erro ao deletar time: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao deletar time")