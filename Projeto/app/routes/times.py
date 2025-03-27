from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from app.services.times_service import TimeService
from app.schemas.schemas import TimeCreate, TimeResponse
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

@router.post("/", response_model=TimeResponse)
def criar_time(time: TimeCreate, db: Session = Depends(get_db)):
    return TimeService.criar_time(db, time)

@router.get("/", response_model=List[TimeResponse])
def listar_times(db: Session = Depends(get_db)):
    return TimeService.listar_times(db)

@router.get("/{time_id}", response_model=TimeResponse)
def obter_time(time_id: int, db: Session = Depends(get_db)):
    return TimeService.obter_time(db, time_id)

@router.put("/{time_id}", response_model=TimeResponse)
def atualizar_time(time_id: int, time: TimeCreate, db: Session = Depends(get_db)):
    return TimeService.atualizar_time(db, time_id, time)

@router.delete("/{time_id}")
def deletar_time(time_id: int, db: Session = Depends(get_db)):
    TimeService.deletar_time(db, time_id)
    return {"detail": "Time deletado com sucesso"}
