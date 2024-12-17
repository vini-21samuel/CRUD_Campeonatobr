from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/partidas", tags=["Partidas"])

# Listar todas as partidas (GET)
@router.get("/", response_model=List[schemas.PartidaResponse])
def listar_partidas(db: Session = Depends(get_db)):
    try:
        return db.query(models.Partida).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar partidas: {str(e)}"
        )

# Buscar partida por ID (GET)
@router.get("/{partida_id}", response_model=schemas.PartidaResponse)
def buscar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )
    return partida

# Criar uma nova partida (POST)
@router.post("/", response_model=schemas.PartidaResponse, status_code=status.HTTP_201_CREATED)
def criar_partida(partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    time1 = db.query(models.Time).filter(models.Time.id == partida.time1_id).first()
    time2 = db.query(models.Time).filter(models.Time.id == partida.time2_id).first()

    if not time1 or not time2:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Times não encontrados")

    db_partida = models.Partida(
        time1_id=partida.time1_id,
        time2_id=partida.time2_id,
        data=partida.data,
        resultado=partida.resultado,
    )
    db.add(db_partida)
    db.commit()
    db.refresh(db_partida)
    return db_partida

# Atualizar uma partida existente (PUT)
@router.put("/{partida_id}", response_model=schemas.PartidaResponse)
def atualizar_partida(partida_id: int, partida: schemas.PartidaCreate, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not db_partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )

    db_partida.time1_id = partida.time1_id
    db_partida.time2_id = partida.time2_id
    db_partida.data = partida.data
    db_partida.resultado = partida.resultado
    db.commit()
    db.refresh(db_partida)
    return db_partida

# Excluir uma partida (DELETE)
@router.delete("/{partida_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_partida(partida_id: int, db: Session = Depends(get_db)):
    db_partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not db_partida:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partida não encontrada"
        )

    db.delete(db_partida)
    db.commit()
    return
