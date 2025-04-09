from pydantic import BaseModel, EmailStr

class UsuarioCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UsuarioLogin(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class Usuario(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
