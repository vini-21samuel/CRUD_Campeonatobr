from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db  # Supondo que você tenha um método get_db para obter a sessão do banco
from app import models

# Instanciar o FastAPI
app = FastAPI()

# Configuração dos templates
templates = Jinja2Templates(directory="app/templates")

# Montar os arquivos estáticos (CSS, JS, imagens, etc.)
app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

# Rota para renderizar a página inicial
@app.get("/", response_class=HTMLResponse)  # Alterando de @router.get para @app.get
async def listar_partidas_html(request: Request, db: Session = Depends(get_db)):
    partidas = db.query(models.Partida).all()  # Buscando todas as partidas
    return templates.TemplateResponse("index.html", {"request": request, "partidas": partidas})

# Rota simples para testar se o servidor está rodando
@app.get("/api")
def root():
    return {"message": "API está rodando!"}

# Incluir routers para outras rotas
from app.routes.times import router as times_router
from app.routes.jogadores import router as jogadores_router
from app.routes.partidas import router as partidas_router

app.include_router(times_router, prefix="/times", tags=["Times"])
app.include_router(jogadores_router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(partidas_router, prefix="/partidas", tags=["Partidas"])
