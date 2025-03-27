from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.time_repository import TimeRepository
from app.schemas.schemas import TimeCreate

class TimeService:
    @staticmethod
    def criar_time(db: Session, time: TimeCreate):
        return TimeRepository.criar_time(db, time)

    @staticmethod
    def listar_times(db: Session):
        return TimeRepository.listar_times(db)

    @staticmethod
    def obter_time(db: Session, time_id: int):
        time = TimeRepository.obter_time(db, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        return time

    @staticmethod
    def atualizar_time(db: Session, time_id: int, time_data: TimeCreate):
        time = TimeRepository.obter_time(db, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        
        return TimeRepository.atualizar_time(db, time_id, time_data)

    @staticmethod
    def deletar_time(db: Session, time_id: int):
        time = TimeRepository.obter_time(db, time_id)
        if not time:
            raise HTTPException(status_code=404, detail="Time não encontrado")
        
        TimeRepository.deletar_time(db, time_id)
