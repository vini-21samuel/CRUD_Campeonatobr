from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from fastapi.templating import Jinja2Templates

# Configuração do Jinja2Templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota HTML: Listar Jogadores
@router.get("/", response_class=HTMLResponse)
async def listar_jogadores_html(request: Request, db: Session = Depends(get_db)):
    jogadores = db.query(models.Jogador).all()
    return templates.TemplateResponse("jogadores.html", {"request": request, "jogadores": jogadores})

# Rota HTML: Formulário para Adicionar Jogador
@router.get("/adicionar", response_class=HTMLResponse)
async def adicionar_jogador(request: Request, db: Session = Depends(get_db)):
    times = db.query(models.Time).all()  # Listar times para vincular ao jogador
    return templates.TemplateResponse("form_jogadores.html", {
        "request": request, "titulo": "Adicionar Jogador", "acao": "/jogadores/adicionar", "times": times
    })

# Rota HTML: Adicionar Jogador
@router.post("/adicionar", response_class=HTMLResponse)
async def salvar_adicao_jogador(
    nome: str = Form(...), 
    posicao: str = Form(...), 
    time_id: int = Form(None), 
    gols: int = Form(...),
    db: Session = Depends(get_db)
):
    # Criar o jogador no banco de dados
    novo_jogador = models.Jogador(
        nome=nome,
        posicao=posicao,
        time_id=time_id,
        gols=gols
    )
    db.add(novo_jogador)
    db.commit()

    return RedirectResponse(url="/jogadores", status_code=303)

# Rota HTML: Atualizar Jogador
@router.get("/editar/{jogador_id}", response_class=HTMLResponse)
async def editar_jogador(request: Request, jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    times = db.query(models.Time).all()
    return templates.TemplateResponse(
        "form_jogadores.html", 
        {"request": request, "jogador": jogador, "titulo": "Editar Jogador", "acao": f"/jogadores/editar/{jogador.id}", "times": times}
    )

@router.post("/editar/{jogador_id}", response_class=HTMLResponse)
async def salvar_edicao_jogador(
    jogador_id: int, 
    nome: str = Form(...), 
    posicao: str = Form(...), 
    time_id: int = Form(None), 
    gols: int = Form(...),
    db: Session = Depends(get_db)
):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    # Atualizar os dados do jogador
    jogador.nome = nome
    jogador.posicao = posicao
    jogador.time_id = time_id
    jogador.gols = gols

    db.commit()
    return RedirectResponse(url="/jogadores", status_code=303)

# Rota para deletar um jogador
@router.post("/deletar/{jogador_id}", response_class=HTMLResponse)
async def deletar_jogador(jogador_id: int, db: Session = Depends(get_db)):
    jogador = db.query(models.Jogador).filter(models.Jogador.id == jogador_id).first()
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")

    db.delete(jogador)
    db.commit()

    return RedirectResponse(url="/jogadores", status_code=303)
