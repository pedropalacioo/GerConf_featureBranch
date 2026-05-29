"""
Testes básicos para a API REST de Biblioteca.
Usa pytest e FastAPI TestClient.
"""
import pytest
import json
import os
import tempfile
from fastapi.testclient import TestClient

from api import app
from src.database import Database
from src.models import Livro

# ==================== Fixtures ====================

@pytest.fixture
def db_temp():
    """Cria um banco de dados temporário para testes"""
    # Cria um arquivo JSON temporário
    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "livros_teste.json")
    
    db = Database(arquivo_dados=db_path)
    yield db
    
    # Limpa após o teste
    if os.path.exists(db_path):
        os.remove(db_path)
    os.rmdir(temp_dir)

@pytest.fixture
def client():
    """Cria um cliente de teste para a API"""
    return TestClient(app)

# ==================== Testes da Classe Livro ====================

def test_livro_criacao():
    """Testa criação de um livro"""
    livro = Livro(id=1, titulo="1984", autor="George Orwell", ano=1949, genero="Ficção")
    
    assert livro.id == 1
    assert livro.titulo == "1984"
    assert livro.autor == "George Orwell"
    assert livro.disponivel == True

def test_livro_to_dict():
    """Testa conversão de livro para dicionário"""
    livro = Livro(id=1, titulo="1984", autor="George Orwell", ano=1949, genero="Ficção", disponivel=False)
    
    livro_dict = livro.to_dict()
    
    assert livro_dict["id"] == 1
    assert livro_dict["titulo"] == "1984"
    assert livro_dict["disponivel"] == False

def test_livro_from_dict():
    """Testa criação de livro a partir de dicionário"""
    dados = {
        "id": 2,
        "titulo": "O Senhor dos Anéis",
        "autor": "J.R.R. Tolkien",
        "ano": 1954,
        "genero": "Fantasia",
        "disponivel": True
    }
    
    livro = Livro.from_dict(dados)
    
    assert livro.titulo == "O Senhor dos Anéis"
    assert livro.autor == "J.R.R. Tolkien"

# ==================== Testes da Classe Database ====================

def test_database_criar_livro(db_temp):
    """Testa criação de um livro no banco"""
    livro = db_temp.criar("Dom Casmurro", "Machado de Assis", 1899, "Romance")
    
    assert livro.id == 1
    assert livro.titulo == "Dom Casmurro"
    assert livro.disponivel == True

def test_database_listar_livros(db_temp):
    """Testa listagem de todos os livros"""
    db_temp.criar("Livro 1", "Autor 1", 2000, "Gênero 1")
    db_temp.criar("Livro 2", "Autor 2", 2001, "Gênero 2")
    
    livros = db_temp.listar()
    
    assert len(livros) == 2
    assert livros[0].titulo == "Livro 1"

def test_database_buscar_por_id(db_temp):
    """Testa busca de livro por ID"""
    db_temp.criar("Test Book", "Test Author", 2020, "Test Genre")
    
    livro = db_temp.buscar_por_id(1)
    
    assert livro is not None
    assert livro.titulo == "Test Book"

def test_database_buscar_por_id_inexistente(db_temp):
    """Testa busca de livro que não existe"""
    livro = db_temp.buscar_por_id(999)
    
    assert livro is None

def test_database_atualizar_livro(db_temp):
    """Testa atualização de um livro"""
    db_temp.criar("Título Original", "Autor Original", 2020, "Gênero Original")
    
    livro_atualizado = db_temp.atualizar(1, titulo="Título Novo")
    
    assert livro_atualizado.titulo == "Título Novo"
    assert livro_atualizado.autor == "Autor Original"

def test_database_deletar_livro(db_temp):
    """Testa deleção de um livro"""
    db_temp.criar("Livro a Deletar", "Autor", 2020, "Gênero")
    
    sucesso = db_temp.deletar(1)
    livros = db_temp.listar()
    
    assert sucesso == True
    assert len(livros) == 0

def test_database_emprestar_devolver(db_temp):
    """Testa emprestar e devolver um livro"""
    db_temp.criar("Livro Emprestável", "Autor", 2020, "Gênero")
    
    livro_emprestado = db_temp.emprestar(1)
    assert livro_emprestado.disponivel == False
    
    livro_devolvido = db_temp.devolver(1)
    assert livro_devolvido.disponivel == True

def test_database_buscar_por_titulo(db_temp):
    """Testa busca por título (parcial, case-insensitive)"""
    db_temp.criar("1984", "George Orwell", 1949, "Ficção")
    db_temp.criar("Fahrenheit 451", "Ray Bradbury", 1953, "Ficção")
    
    resultados = db_temp.buscar_por_titulo("984")
    
    assert len(resultados) == 1
    assert resultados[0].titulo == "1984"

def test_database_listar_disponiveis(db_temp):
    """Testa listagem de livros disponíveis"""
    db_temp.criar("Livro 1", "Autor 1", 2020, "Gênero 1")
    livro2 = db_temp.criar("Livro 2", "Autor 2", 2020, "Gênero 2")
    
    db_temp.emprestar(livro2.id)
    
    disponiveis = db_temp.listar_disponiveis()
    
    assert len(disponiveis) == 1
    assert disponiveis[0].titulo == "Livro 1"

# ==================== Testes da API REST ====================

def test_api_raiz(client):
    """Testa endpoint raiz"""
    response = client.get("/")
    
    assert response.status_code == 200
    assert "mensagem" in response.json()

def test_api_criar_livro(client):
    """Testa criação de livro via API"""
    payload = {
        "titulo": "Novo Livro",
        "autor": "Novo Autor",
        "ano": 2025,
        "genero": "Ficção"
    }
    
    response = client.post("/livros", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["titulo"] == "Novo Livro"
    assert data["id"] == 1

def test_api_listar_livros(client):
    """Testa listagem de livros via API"""
    # Criar alguns livros
    client.post("/livros", json={"titulo": "Livro 1", "autor": "Autor 1", "ano": 2020, "genero": "Gênero 1"})
    client.post("/livros", json={"titulo": "Livro 2", "autor": "Autor 2", "ano": 2021, "genero": "Gênero 2"})
    
    response = client.get("/livros")
    
    assert response.status_code == 200
    livros = response.json()
    assert len(livros) == 2

def test_api_obter_livro(client):
    """Testa obtenção de um livro específico"""
    # Criar um livro
    client.post("/livros", json={"titulo": "Livro Test", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    
    response = client.get("/livros/1")
    
    assert response.status_code == 200
    assert response.json()["titulo"] == "Livro Test"

def test_api_obter_livro_inexistente(client):
    """Testa obtenção de livro que não existe"""
    response = client.get("/livros/999")
    
    assert response.status_code == 404

def test_api_atualizar_livro(client):
    """Testa atualização de livro via API"""
    # Criar um livro
    client.post("/livros", json={"titulo": "Título Original", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    
    # Atualizar
    response = client.put("/livros/1", json={"titulo": "Título Atualizado"})
    
    assert response.status_code == 200
    assert response.json()["titulo"] == "Título Atualizado"

def test_api_deletar_livro(client):
    """Testa deleção de livro via API"""
    # Criar um livro
    client.post("/livros", json={"titulo": "Livro", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    
    # Deletar
    response = client.delete("/livros/1")
    
    assert response.status_code == 204
    
    # Verificar que foi deletado
    response_get = client.get("/livros/1")
    assert response_get.status_code == 404

def test_api_emprestar_livro(client):
    """Testa empréstimo de livro via API"""
    # Criar um livro
    client.post("/livros", json={"titulo": "Livro", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    
    # Emprestar
    response = client.post("/livros/1/emprestar")
    
    assert response.status_code == 200
    assert response.json()["disponivel"] == False

def test_api_devolver_livro(client):
    """Testa devolução de livro via API"""
    # Criar e emprestar um livro
    client.post("/livros", json={"titulo": "Livro", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    client.post("/livros/1/emprestar")
    
    # Devolver
    response = client.post("/livros/1/devolver")
    
    assert response.status_code == 200
    assert response.json()["disponivel"] == True

def test_api_listar_disponiveis(client):
    """Testa listagem de livros disponíveis via API"""
    # Criar dois livros
    client.post("/livros", json={"titulo": "Livro 1", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    client.post("/livros", json={"titulo": "Livro 2", "autor": "Autor", "ano": 2020, "genero": "Gênero"})
    
    # Emprestar o segundo
    client.post("/livros/2/emprestar")
    
    # Listar disponíveis
    response = client.get("/livros/disponiveis")
    
    assert response.status_code == 200
    livros = response.json()
    assert len(livros) == 1
    assert livros[0]["titulo"] == "Livro 1"

def test_api_buscar_por_titulo(client):
    """Testa busca por título via API"""
    # Criar livros
    client.post("/livros", json={"titulo": "1984", "autor": "George Orwell", "ano": 1949, "genero": "Ficção"})
    client.post("/livros", json={"titulo": "Fahrenheit 451", "autor": "Ray Bradbury", "ano": 1953, "genero": "Ficção"})
    
    # Buscar
    response = client.get("/livros/busca/titulo?q=1984")
    
    assert response.status_code == 200
    livros = response.json()
    assert len(livros) == 1
    assert livros[0]["titulo"] == "1984"

def test_api_buscar_por_autor(client):
    """Testa busca por autor via API"""
    # Criar livros
    client.post("/livros", json={"titulo": "1984", "autor": "George Orwell", "ano": 1949, "genero": "Ficção"})
    client.post("/livros", json={"titulo": "Animal Farm", "autor": "George Orwell", "ano": 1945, "genero": "Ficção"})
    
    # Buscar
    response = client.get("/livros/busca/autor?q=Orwell")
    
    assert response.status_code == 200
    livros = response.json()
    assert len(livros) == 2
