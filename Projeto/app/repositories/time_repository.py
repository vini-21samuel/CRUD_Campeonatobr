from sqlalchemy.orm import Session
from app.models.models import Time
from app.schemas.schemas import TimeCreate

class TimeRepository:
    @staticmethod
    def criar_time(db: Session, time: TimeCreate):
        novo_time = Time(nome=time.nome, lugar=time.lugar)
        db.add(novo_time)
        db.commit()
        db.refresh(novo_time)
        return novo_time

    @staticmethod
    def listar_times(db: Session):
        return db.query(Time).all()

    @staticmethod
    def obter_time(db: Session, time_id: int):
        return db.query(Time).filter(Time.id == time_id).first()

    @staticmethod
    def atualizar_time(db: Session, time_id: int, time_data: TimeCreate):
        time = db.query(Time).filter(Time.id == time_id).first()
        if time:
            time.nome = time_data.nome
            time.lugar = time_data.lugar
            db.commit()
            db.refresh(time)
        return time

    @staticmethod
    def deletar_time(db: Session, time_id: int):
        time = db.query(Time).filter(Time.id == time_id).first()
        if time:
            db.delete(time)
            db.commit()
