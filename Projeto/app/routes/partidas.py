from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from app import models
from app.database import get_db
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

# Rota para listar todas as partidas
@router.get("/", response_class=HTMLResponse)
async def listar_partidas(request: Request, db: Session = Depends(get_db)):
    partidas = db.query(models.Partida).all()
    return templates.TemplateResponse("partidas.html", {"request": request, "partidas": partidas})

# Rota para exibir o formulário de adicionar uma nova partida
@router.get("/adicionar", response_class=HTMLResponse)
async def adicionar_partida(request: Request, db: Session = Depends(get_db)):
    times = db.query(models.Time).all()  # Buscar todos os times
    return templates.TemplateResponse("form_partidas.html", {
        "request": request, "titulo": "Adicionar Partida", "acao": "/partidas/adicionar", "times": times
    })

# Rota para salvar a nova partida
@router.post("/adicionar", response_class=HTMLResponse)
async def salvar_partida(
    data: str = Form(...), 
    time1_id: int = Form(...), 
    time2_id: int = Form(...), 
    resultado: str = Form(None), 
    db: Session = Depends(get_db)
):
    nova_partida = models.Partida(data=data, time1_id=time1_id, time2_id=time2_id, resultado=resultado)
    db.add(nova_partida)
    db.commit()
    return RedirectResponse(url="/partidas", status_code=303)

# Rota para exibir o formulário de edição de uma partida existente
@router.get("/editar/{partida_id}", response_class=HTMLResponse)
async def editar_partida(request: Request, partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    times = db.query(models.Time).all()  # Buscar todos os times
    return templates.TemplateResponse(
        "form_partidas.html", 
        {"request": request, "partida": partida, "titulo": "Editar Partida", "acao": f"/partidas/editar/{partida.id}", "times": times}
    )

# Rota para salvar a edição de uma partida existente
@router.post("/editar/{partida_id}", response_class=HTMLResponse)
async def salvar_edicao_partida(
    partida_id: int, 
    data: str = Form(...), 
    time1_id: int = Form(...), 
    time2_id: int = Form(...), 
    resultado: str = Form(None), 
    db: Session = Depends(get_db)
):
    partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    partida.data = data
    partida.time1_id = time1_id
    partida.time2_id = time2_id
    partida.resultado = resultado
    db.commit()
    
    return RedirectResponse(url="/partidas", status_code=303)

# Rota para deletar uma partida
@router.get("/deletar/{partida_id}", response_class=HTMLResponse)
async def deletar_partida(partida_id: int, db: Session = Depends(get_db)):
    partida = db.query(models.Partida).filter(models.Partida.id == partida_id).first()
    if not partida:
        raise HTTPException(status_code=404, detail="Partida não encontrada")
    
    db.delete(partida)
    db.commit()
    
    return RedirectResponse(url="/partidas", status_code=303)
