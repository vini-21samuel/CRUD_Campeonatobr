from sqlalchemy.orm import Session
from sqlalchemy.orm import aliased
from app.models.models import Partida, Time
from app.schemas.schemas import PartidaCreate

class PartidaRepository:


    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate):
        nova_partida = Partida(
            time1_id=partida.time1_id,
            time2_id=partida.time2_id,
            data=partida.data,
            resultado=partida.resultado
        )
        db.add(nova_partida)
        db.commit()
        db.refresh(nova_partida)
        return nova_partida

    @staticmethod
    def listar_partidas(db):
        Time1 = aliased(Time)
        Time2 = aliased(Time)
    
        return db.query(
            Partida.id, 
            Partida.data, 
            Partida.resultado, 
            Time1.nome.label("time1_nome"), 
            Time2.nome.label("time2_nome")
        ).join(Time1, Partida.time1_id == Time1.id
        ).join(Time2, Partida.time2_id == Time2.id
        ).all()

    @staticmethod
    def obter_partida(db: Session, partida_id: int):
        return db.query(
            Partida.id,
            Partida.data,
            Partida.resultado,
            Time.nome.label("time1_nome"),
            Time.nome.label("time2_nome")
        ).join(Time, Partida.time1_id == Time.id).join(Time, Partida.time2_id == Time.id).filter(Partida.id == partida_id).first()

    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if partida:
            db.delete(partida)
            db.commit()
