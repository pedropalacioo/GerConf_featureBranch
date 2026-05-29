"""
API REST para o sistema de biblioteca usando FastAPI.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.database import Database
from src.models import Livro

app = FastAPI(title="Biblioteca API", version="1.0.0")

# CORS - Permite requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa banco de dados
db = Database()

# ==================== Modelos Pydantic ====================

class LivroCreate(BaseModel):
    """Modelo para criar livro"""
    titulo: str
    autor: str
    ano: int
    genero: str

class LivroUpdate(BaseModel):
    """Modelo para atualizar livro"""
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    genero: Optional[str] = None
    disponivel: Optional[bool] = None

class LivroResponse(BaseModel):
    """Modelo de resposta"""
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str
    disponivel: bool

    class Config:
        from_attributes = True

# ==================== Endpoints ====================

@app.get("/")
def raiz():
    """Health check"""
    return {"mensagem": "API Biblioteca funcionando ✓"}

# GET - Listar todos os livros
@app.get("/livros", response_model=list[LivroResponse])
def listar_livros():
    """Lista todos os livros"""
    livros = db.listar()
    return [l.to_dict() for l in livros]

# GET - Listar apenas livros disponíveis
@app.get("/livros/disponiveis", response_model=list[LivroResponse])
def listar_disponiveis():
    """Lista apenas livros disponíveis"""
    livros = db.listar_disponiveis()
    return [l.to_dict() for l in livros]

# GET - Buscar por ID
@app.get("/livros/{livro_id}", response_model=LivroResponse)
def obter_livro(livro_id: int):
    """Obtém um livro por ID"""
    livro = db.buscar_por_id(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro.to_dict()

# POST - Criar novo livro
@app.post("/livros", response_model=LivroResponse, status_code=201)
def criar_livro(livro: LivroCreate):
    """Cria um novo livro"""
    novo_livro = db.criar(livro.titulo, livro.autor, livro.ano, livro.genero)
    return novo_livro.to_dict()

# PUT - Atualizar livro
@app.put("/livros/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, livro: LivroUpdate):
    """Atualiza um livro existente"""
    dados_atualizacao = {k: v for k, v in livro.model_dump().items() if v is not None}
    livro_atualizado = db.atualizar(livro_id, **dados_atualizacao)
    if not livro_atualizado:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro_atualizado.to_dict()

# DELETE - Deletar livro
@app.delete("/livros/{livro_id}", status_code=204)
def deletar_livro(livro_id: int):
    """Deleta um livro"""
    sucesso = db.deletar(livro_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

# POST - Emprestar livro
@app.post("/livros/{livro_id}/emprestar", response_model=LivroResponse)
def emprestar_livro(livro_id: int):
    """Marca um livro como emprestado"""
    livro = db.emprestar(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro.to_dict()

# POST - Devolver livro
@app.post("/livros/{livro_id}/devolver", response_model=LivroResponse)
def devolver_livro(livro_id: int):
    """Marca um livro como devolvido"""
    livro = db.devolver(livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro.to_dict()

# GET - Buscar por título
@app.get("/livros/busca/titulo", response_model=list[LivroResponse])
def buscar_titulo(q: str):
    """Busca livros por título (parcial, case-insensitive)"""
    livros = db.buscar_por_titulo(q)
    return [l.to_dict() for l in livros]

# GET - Buscar por autor
@app.get("/livros/busca/autor", response_model=list[LivroResponse])
def buscar_autor(q: str):
    """Busca livros por autor (parcial, case-insensitive)"""
    livros = db.buscar_por_autor(q)
    return [l.to_dict() for l in livros]
