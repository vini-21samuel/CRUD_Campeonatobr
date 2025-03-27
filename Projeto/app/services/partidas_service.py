from sqlalchemy.orm import Session
from app.models.models import Partida, Time
from app.schemas.schemas import PartidaCreate, PartidaResponse

class PartidaService:

    @staticmethod
    def criar_partida(db: Session, partida: PartidaCreate) -> PartidaResponse:
        db_partida = Partida(**partida.dict())
        db.add(db_partida)
        db.commit()
        db.refresh(db_partida)  

        # Buscar os nomes dos times
        time1 = db.query(Time).filter(Time.id == db_partida.time1_id).first()
        time2 = db.query(Time).filter(Time.id == db_partida.time2_id).first()

        # Retornar no formato esperado
        return PartidaResponse(
            id=db_partida.id,
            time1_nome=time1.nome if time1 else "Desconhecido",
            time2_nome=time2.nome if time2 else "Desconhecido",
            data=db_partida.data.strftime("%Y-%m-%d"),  # Converte para string no formato correto
            resultado=db_partida.resultado
        )

    @staticmethod
    def listar_partidas(db: Session):
        partidas = db.query(Partida).all()
        return [
            PartidaResponse(
                id=partida.id,
                time1_nome=db.query(Time).filter(Time.id == partida.time1_id).first().nome,
                time2_nome=db.query(Time).filter(Time.id == partida.time2_id).first().nome,
                data=partida.data.strftime("%Y-%m-%d"),
                resultado=partida.resultado
            ) for partida in partidas
        ]

    @staticmethod
    def obter_partida(db: Session, partida_id: int) -> PartidaResponse:
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if not partida:
            return None

        time1 = db.query(Time).filter(Time.id == partida.time1_id).first()
        time2 = db.query(Time).filter(Time.id == partida.time2_id).first()

        return PartidaResponse(
            id=partida.id,
            time1_nome=time1.nome if time1 else "Desconhecido",
            time2_nome=time2.nome if time2 else "Desconhecido",
            data=partida.data.strftime("%Y-%m-%d"),
            resultado=partida.resultado
        )

    @staticmethod
    def deletar_partida(db: Session, partida_id: int):
        partida = db.query(Partida).filter(Partida.id == partida_id).first()
        if partida:
            db.delete(partida)
            db.commit()
