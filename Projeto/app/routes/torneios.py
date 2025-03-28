from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.models import Torneio
from database.database import get_db
from app.services.torneios_services import TorneioService
from app.schemas.schemas import TorneioResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def pagina_torneios(request):
    return templates.TemplateResponse("torneios.html", {"request": request})

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
            "capa": f"/static/imagens/torneios/{t.capa}" if t.capa else "/static/imagens/default.jpg"
        }
        for t in torneios
    ]


# 📌 Criar torneio
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

        # Garante que o caminho completo da capa seja retornado corretamente
        return {
            "id": novo_torneio.id,
            "nome": novo_torneio.nome,
            "organizador": novo_torneio.organizador,
            "data_inicio": novo_torneio.data_inicio.strftime("%Y-%m-%d"),
            "descricao": novo_torneio.descricao,
            "formato": novo_torneio.formato,
            "capa": f"/static/imagens/torneios/{novo_torneio.capa}" if novo_torneio.capa else "/static/imagens/default.jpg"
        }

    except Exception as e:
        print(f"Erro ao criar torneio: {e}")
        raise HTTPException(status_code=500, detail="Erro interno ao criar torneio.")


@router.get("/torneios/{torneio_id}")
def obter_torneio(torneio_id: int, db: Session = Depends(get_db)):
    torneio = db.query(Torneio).filter(Torneio.id == torneio_id).first()
    if not torneio:
        raise HTTPException(status_code=404, detail="Torneio não encontrado.")
    return torneio

@router.put("/torneios/{torneio_id}")
async def editar_torneio(
    torneio_id: int,
    nome: str = Form(None),
    organizador: str = Form(None),
    data_inicio: str = Form(None),
    descricao: str = Form(None),
    formato: str = Form(None),
    capa: UploadFile = None,
    db: Session = Depends(get_db)
):
    try:
        torneio_atualizado = TorneioService.editar_torneio(
            db, torneio_id, nome, organizador, data_inicio, descricao, formato, capa
        )
        return {"message": "Torneio atualizado com sucesso", "torneio": torneio_atualizado}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 📌 Deletar torneio
@router.delete("/{torneio_id}")
def deletar_torneio(torneio_id: int, db: Session = Depends(get_db)):
    try:
        TorneioService.deletar_torneio(db, torneio_id)
        return JSONResponse(content={"message": "Torneio deletado com sucesso."}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Erro interno ao deletar torneio.")
