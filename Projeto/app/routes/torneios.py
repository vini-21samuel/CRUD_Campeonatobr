from fastapi import APIRouter, Depends, HTTPException, Form, Request, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.models.torneio import Torneio
from app.database.database import get_db, SessionLocal
from app.services.torneios_services import TorneioService
from app.schemas.torneio import TorneioResponse, TorneioUpdate
from fastapi.templating import Jinja2Templates
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota para a página inicial de torneios
@router.get("/", response_class=HTMLResponse)
async def pagina_torneios(request: Request):
    return templates.TemplateResponse("torneios.html", {"request": request})

# Rota para listar os torneios em formato JSON
@router.get("/dados", response_model=List[TorneioResponse])
def listar_torneios(db: Session = Depends(get_db)):
    torneios = TorneioService.listar_torneios(db)
    return [
        {
            "id": t.id,
            "nome": t.nome,
            "organizador": t.organizador,
            "data_inicio": t.data_inicio.strftime("%Y-%m-%d"),
            "descricao": t.descricao,
            "formato": t.formato,
            "numGrupos": t.numGrupos,
            "numClassificados": t.numClassificados,
            "capa": f"/static/imagens/torneios/{t.capa}" if t.capa else "/static/imagens/default.jpg"
        }
        for t in torneios
    ]

# Rota para criar um torneio
@router.post("/", response_model=TorneioResponse, status_code=201)
def criar_torneio(
    nome: str = Form(...),
    organizador: str = Form(...),
    data_inicio: str = Form(...),
    descricao: str = Form(None),
    formato: str = Form(...),
    capa: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        novo_torneio = TorneioService.criar_torneio(db, nome, organizador, data_inicio, descricao, formato, capa)
        return {
            "id": novo_torneio.id,
            "nome": novo_torneio.nome,
            "organizador": novo_torneio.organizador,
            "data_inicio": novo_torneio.data_inicio.strftime("%Y-%m-%d"),
            "descricao": novo_torneio.descricao,
            "formato": novo_torneio.formato,
            "numGrupos": novo_torneio.numGrupos,
            "numClassificados": novo_torneio.numClassificados,
            "capa": f"/static/imagens/torneios/{novo_torneio.capa}" if novo_torneio.capa else "/static/imagens/default.jpg"
        }
    except Exception as e:
        print(f"Erro ao criar torneio: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar torneio.")

# Rota para obter um torneio específico
@router.get("/torneios/{torneio_id}", response_model=TorneioResponse)
def obter_torneio(torneio_id: int, db: Session = Depends(get_db)):
    torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
    if not torneio:
        raise HTTPException(status_code=404, detail="Torneio não encontrado.")
    return {
        "id": torneio.id,
        "nome": torneio.nome,
        "organizador": torneio.organizador,
        "data_inicio": torneio.data_inicio.strftime("%Y-%m-%d"),
        "descricao": torneio.descricao,
        "formato": torneio.formato,
        "numGrupos": torneio.numGrupos,
        "numClassificados": torneio.numClassificados,
        "capa": f"/static/imagens/torneios/{torneio.capa}" if torneio.capa else "/static/imagens/default.jpg"
    }

# Rota para editar um torneio
@router.put("/torneios/{torneio_id}", response_model=TorneioResponse)
async def editar_torneio(
    torneio_id: int,
    torneio_update: TorneioUpdate,
    db: Session = Depends(get_db)
):
    torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
    if not torneio:
        raise HTTPException(status_code=404, detail="Torneio não encontrado.")
    
    update_data = torneio_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(torneio, key, value)
    
    db.commit()
    db.refresh(torneio)
    return {
        "id": torneio.id,
        "nome": torneio.nome,
        "organizador": torneio.organizador,
        "data_inicio": torneio.data_inicio.strftime("%Y-%m-%d"),
        "descricao": torneio.descricao,
        "formato": torneio.formato,
        "numGrupos": torneio.numGrupos,
        "numClassificados": torneio.numClassificados,
        "capa": f"/static/imagens/torneios/{torneio.capa}" if torneio.capa else "/static/imagens/default.jpg"
    }

# Rota para deletar um torneio
@router.delete("/torneios/{torneio_id}")
def deletar_torneio(torneio_id: int, db: Session = Depends(get_db)):
    try:
        TorneioService.deletar_torneio(db, torneio_id)
        return JSONResponse(content={"message": "Torneio deletado com sucesso."}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao deletar torneio.")

# Rota para gerenciar torneio
@router.get("/gerenciar_torneio/{torneio_id}", response_class=HTMLResponse)
async def gerenciar_torneio(request: Request, torneio_id: int, db: Session = Depends(get_db)):
    torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
    if not torneio:
        raise HTTPException(status_code=404, detail="Torneio não encontrado.")
    
    return templates.TemplateResponse(
        "gerenciar_torneio.html",
        {
            "request": request,
            "torneio": {
                "id": torneio.id,
                "nome": torneio.nome,
                "organizador": torneio.organizador,
                "data_inicio": torneio.data_inicio.strftime("%Y-%m-%d"),
                "formato": torneio.formato,
                "numGrupos": torneio.numGrupos,
                "numClassificados": torneio.numClassificados,
                "descricao": torneio.descricao or "Sem descrição.",
                "capa": f"/static/imagens/torneios/{torneio.capa}" if torneio.capa else "/static/imagens/default.jpg"
            }
        }
    )

# Rota para listar campeonatos
@router.get("/campeonatos", response_class=HTMLResponse)
async def get_campeonatos(request: Request):
    return templates.TemplateResponse("campeonatos.html", {"request": request})

# Rota para listar dados de campeonatos
@router.get("/campeonatos/dados", response_model=List[TorneioResponse])
def listar_torneios_campeonatos(db: Session = Depends(get_db)):
    torneios = TorneioService.listar_torneios(db)
    print("Torneios retornados:", torneios)  
    return [
        {
            "id": t.id,
            "nome": t.nome,
            "organizador": t.organizador,
            "data_inicio": t.data_inicio.strftime("%Y-%m-%d"),
            "descricao": t.descricao,
            "formato": t.formato,
            "numGrupos": t.numGrupos,
            "numClassificados": t.numClassificados,
            "capa": f"/static/imagens/torneios/{t.capa}" if t.capa else "/static/imagens/default.jpg"
        }
        for t in torneios
    ]

# Rota para a página "Sobre"
@router.get("/sobre", response_class=HTMLResponse)
async def get_sobre(request: Request):
    return templates.TemplateResponse("sobre.html", {"request": request})

# Rota para configurar campeonato
@router.get("/configurar_campeonato/{torneio_id}", response_class=HTMLResponse)
async def configurar_campeonato(request: Request, torneio_id: int, db: Session = Depends(get_db)):
    torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
    if not torneio:
        raise HTTPException(status_code=404, detail="Torneio não encontrado.")
    return templates.TemplateResponse(
        "configurar_campeonato.html",
        {
            "request": request,
            "torneio": {
                "id": torneio.id,
                "nome": torneio.nome,
                "formato": torneio.formato,
                "organizador": torneio.organizador,
                "data_inicio": torneio.data_inicio.strftime("%Y-%m-%d"),
                "numGrupos": torneio.numGrupos,
                "numClassificados": torneio.numClassificados,
                "descricao": torneio.descricao or "Sem descrição.",
                "capa": f"/static/imagens/torneios/{torneio.capa}" if torneio.capa else "/static/imagens/default.jpg"
            }
        }
    )