"""
Gerenciamento de banco de dados para livros.
"""

import json
import os
from .models import Livro, Usuario

class Database:
    """Gerencia o armazenamento e recuperação de livros."""
    
    def __init__(self, arquivo_dados='data/livros.json'):
        self.arquivo_dados = arquivo_dados
        self._garantir_arquivo()
    
    def _garantir_arquivo(self):
        """Garante que o arquivo de dados existe."""
        os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)
        if not os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _carregar(self):
        """Carrega todos os livros do arquivo."""
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return [Livro.from_dict(item) for item in dados]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _salvar(self, livros):
        """Salva todos os livros no arquivo."""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            dados = [livro.to_dict() for livro in livros]
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def _proxima_id(self):
        """Gera o próximo ID disponível."""
        livros = self._carregar()
        if not livros:
            return 1
        return max(livro.id for livro in livros) + 1
    
    # ==================== CRUD ====================
    
    def criar(self, titulo, autor, ano, genero):
        """Cria um novo livro na biblioteca."""
        livros = self._carregar()
        novo_id = self._proxima_id()
        novo_livro = Livro(
            id=novo_id,
            titulo=titulo,
            autor=autor,
            ano=ano,
            genero=genero
        )
        livros.append(novo_livro)
        self._salvar(livros)
        return novo_livro
    
    def listar(self):
        """Retorna todos os livros."""
        return self._carregar()
    
    def listar_disponiveis(self):
        """Retorna apenas livros disponíveis."""
        livros = self._carregar()
        return [livro for livro in livros if livro.disponivel]
    
    def buscar_por_id(self, livro_id):
        """Busca um livro pelo ID."""
        livros = self._carregar()
        for livro in livros:
            if livro.id == livro_id:
                return livro
        return None
    
    def buscar_por_titulo(self, titulo):
        """Busca livros pelo título (busca parcial)."""
        livros = self._carregar()
        return [livro for livro in livros if titulo.lower() in livro.titulo.lower()]
    
    def buscar_por_autor(self, autor):
        """Busca livros pelo autor (busca parcial)."""
        livros = self._carregar()
        return [livro for livro in livros if autor.lower() in livro.autor.lower()]
    
    def atualizar(self, livro_id, titulo=None, autor=None, ano=None, genero=None, disponivel=None):
        """Atualiza um livro existente."""
        livros = self._carregar()
        for livro in livros:
            if livro.id == livro_id:
                if titulo is not None:
                    livro.titulo = titulo
                if autor is not None:
                    livro.autor = autor
                if ano is not None:
                    livro.ano = ano
                if genero is not None:
                    livro.genero = genero
                if disponivel is not None:
                    livro.disponivel = disponivel
                self._salvar(livros)
                return livro
        return None
    
    def deletar(self, livro_id):
        """Deleta um livro da biblioteca."""
        livros = self._carregar()
        livros_filtrados = [livro for livro in livros if livro.id != livro_id]
        if len(livros_filtrados) < len(livros):
            self._salvar(livros_filtrados)
            return True
        return False
    
    def emprestar(self, livro_id):
        """Marca um livro como emprestado."""
        return self.atualizar(livro_id, disponivel=False)
    
    def devolver(self, livro_id):
        """Marca um livro como devolvido (disponível)."""
        return self.atualizar(livro_id, disponivel=True)

class UsuarioDatabase:
    """Gerencia o armazenamento e recuperação de usuários."""
    
    def __init__(self, arquivo_dados='data/usuarios.json'):
        self.arquivo_dados = arquivo_dados
        self._garantir_arquivo()
    
    def _garantir_arquivo(self):
        """Garante que o arquivo de dados existe."""
        os.makedirs(os.path.dirname(self.arquivo_dados), exist_ok=True)
        if not os.path.exists(self.arquivo_dados):
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
    
    def _carregar(self):
        """Carrega todos os usuários do arquivo."""
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                return [Usuario.from_dict(item) for item in dados]
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _salvar(self, usuarios):
        """Salva todos os usuários no arquivo."""
        with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
            dados = [usuario.to_dict() for usuario in usuarios]
            json.dump(dados, f, ensure_ascii=False, indent=2)
    
    def _proxima_id(self):
        """Gera o próximo ID disponível."""
        usuarios = self._carregar()
        if not usuarios:
            return 1
        return max(usuario.id for usuario in usuarios) + 1
    
    def criar_usuario(self, nome, username, senha):
        """Cria um novo usuário."""
        if self.buscar_por_username(username):
            return None # Usuário já existe
            
        usuarios = self._carregar()
        novo_usuario = Usuario(
            id=self._proxima_id(),
            nome=nome,
            username=username,
            senha=senha
        )
        usuarios.append(novo_usuario)
        self._salvar(usuarios)
        return novo_usuario
    
    def buscar_por_username(self, username):
        """Busca um usuário pelo username."""
        usuarios = self._carregar()
        for usuario in usuarios:
            if usuario.username == username:
                return usuario
        return None

    def autenticar(self, username, senha):
        """Autentica um usuário."""
        usuario = self.buscar_por_username(username)
        if usuario and usuario.senha == senha:
            return usuario
        return None

    def registrar_emprestimo(self, usuario_id, livro):
        """Registra um empréstimo no histórico do usuário."""
        usuarios = self._carregar()
        for usuario in usuarios:
            if usuario.id == usuario_id:
                # Adiciona livro ao histórico com status 'pendente'
                usuario.historico.append({
                    'livro_id': livro.id,
                    'titulo': livro.titulo,
                    'status': 'pendente'
                })
                self._salvar(usuarios)
                return True
        return False

    def registrar_devolucao(self, usuario_id, livro_id):
        """Registra uma devolução no histórico do usuário."""
        usuarios = self._carregar()
        for usuario in usuarios:
            if usuario.id == usuario_id:
                for item in usuario.historico:
                    if item['livro_id'] == livro_id and item['status'] == 'pendente':
                        item['status'] = 'devolvido'
                        self._salvar(usuarios)
                        return True
        return False
