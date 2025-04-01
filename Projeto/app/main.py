from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from database.database import get_db
from app.utils.auth import decode_token  # Importando a função correta
from app.models.models import Torneio  # Supondo que você tenha um modelo Torneio

# Instanciando o FastAPI
app = FastAPI()

# Configuração de templates Jinja2
templates = Jinja2Templates(directory="app/templates")

# Serve arquivos estáticos (CSS, imagens, etc.)
app.mount("/static", StaticFiles(directory="app/templates/static/"), name="static")

# Rota para renderizar a página inicial
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token or not decode_token(token):  # Usa a função para validar o token
        return RedirectResponse(url="/usuarios/login", status_code=303)

    # Buscar torneios no banco de dados (ajuste conforme a lógica de seu sistema)
    torneios = db.query(Torneio).all()  # Exemplo de consulta para pegar todos os torneios

    # Passando os dados para o template
    return templates.TemplateResponse("base.html", {"request": request, "torneios": torneios})

# Importação das rotas após a criação do `app`
from app.routes.times import router as times_router
from app.routes.jogadores import router as jogadores_router
from app.routes.partidas import router as partidas_router
from app.routes.usuarios import router as usuarios_router
from app.routes.torneios import router as torneios_router

# Incluindo as rotas no FastAPI
app.include_router(usuarios_router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(times_router, prefix="/times", tags=["Times"])
app.include_router(jogadores_router, prefix="/jogadores", tags=["Jogadores"])
app.include_router(partidas_router, prefix="/partidas", tags=["Partidas"])
app.include_router(torneios_router, prefix="/torneios", tags=["Torneios"])
