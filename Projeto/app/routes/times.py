from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from fastapi.templating import Jinja2Templates  # Adicionando Jinja2Templates
from app.models import Partida  # Adicionando o modelo Partida


# Configuração do Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

# Função para obter todas as partidas
def get_partida(db: Session):
    return db.query(Partida).all()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## Rota HTML: Listar Times
@router.get("/", response_class=HTMLResponse)
async def listar_times_html(request: Request, db: Session = Depends(get_db)):
    times = db.query(models.Time).all()
    return templates.TemplateResponse("times.html", {"request": request, "times": times})

# Rota HTML: Formulário para Adicionar Time
@router.get("/adicionar", response_class=HTMLResponse)
async def adicionar_time(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request, "titulo": "Adicionar Time", "acao": "/times/adicionar"
    })

# Rota HTML: Adicionar Time
@router.post("/adicionar", response_class=HTMLResponse)
async def salvar_adicao_time(nome: str = Form(...), lugar: str = Form(...), db: Session = Depends(get_db)):
    # Criação de um novo time
    novo_time = models.Time(nome=nome, lugar=lugar)
    db.add(novo_time)
    db.commit()
    
    return RedirectResponse(url="/times", status_code=303)


# Rota HTML: Atualizar Time
@router.get("/editar/{time_id}", response_class=HTMLResponse)
async def editar_time(request: Request, time_id: int, db: Session = Depends(get_db)):
    time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    return templates.TemplateResponse(
        "form.html", 
        {"request": request, "time": time, "titulo": "Editar Time", "acao": f"/times/editar/{time.id}"}
    )

@router.post("/editar/{time_id}", response_class=HTMLResponse)
async def salvar_edicao_time(time_id: int, nome: str = Form(...), lugar: str = Form(...), db: Session = Depends(get_db)):
    time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    
    time.nome = nome
    time.lugar = lugar
    db.commit()
    
    return RedirectResponse(url="/times", status_code=303)

# Rota HTML: Excluir Time
@router.post("/deletar/{time_id}")
async def deletar_time(time_id: int, db: Session = Depends(get_db)):
    time = db.query(models.Time).filter(models.Time.id == time_id).first()
    if not time:
        raise HTTPException(
            status_code=404, detail="Time não encontrado para exclusão."
        )
    db.delete(time)
    db.commit()
    return RedirectResponse(url="/times", status_code=303)
