from fastapi import APIRouter, Depends, HTTPException, status, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from database.database import SessionLocal
from fastapi.templating import Jinja2Templates
from app.models.models import Usuario  # Importação correta
from app.schemas.schemas import UsuarioCreate, UsuarioLogin
from app.auth import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Função para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rota HTML: Formulário de Cadastro
@router.get("/cadastrar", response_class=HTMLResponse)
async def cadastrar_form(request: Request):
    return templates.TemplateResponse("cadastrar.html", {"request": request})

# Rota para cadastrar usuário
@router.post("/cadastrar", response_class=HTMLResponse)
async def cadastrar_usuario(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    # Verifica se o e-mail já está cadastrado
    existing_user = db.query(Usuario).filter(Usuario.email == email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")

    # Criptografa a senha
    hashed_password = get_password_hash(password)

    # Cria um novo usuário
    new_user = Usuario(
        name=name,
        username=username,
        phone=phone,
        email=email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return RedirectResponse(url="/usuarios/login", status_code=303)

# Rota HTML: Formulário de Login
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Rota para autenticação de usuário
@router.post("/login", response_class=HTMLResponse)
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    # Busca usuário pelo e-mail
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos")

    # Gera token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
