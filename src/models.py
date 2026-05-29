"""
Modelos de dados para o sistema de biblioteca.
"""

class Livro:
    """Modelo representando um livro na biblioteca."""
    
    def __init__(self, id, titulo, autor, ano, genero, disponivel=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.genero = genero
        self.disponivel = disponivel
    
    def __str__(self):
        status = "Disponível" if self.disponivel else "Indisponível"
        return f"[{self.id}] {self.titulo} - {self.autor} ({self.ano}) | Gênero: {self.genero} | Status: {status}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Converte o livro para dicionário."""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'autor': self.autor,
            'ano': self.ano,
            'genero': self.genero,
            'disponivel': self.disponivel
        }
    
    @staticmethod
    def from_dict(data):
        """Cria um livro a partir de um dicionário."""
        return Livro(
            id=data['id'],
            titulo=data['titulo'],
            autor=data['autor'],
            ano=data['ano'],
            genero=data['genero'],
            disponivel=data.get('disponivel', True)
        )

class Usuario:
    """Modelo representando um usuário do sistema."""
    
    def __init__(self, id, nome, username, senha, historico=None):
        self.id = id
        self.nome = nome
        self.username = username
        self.senha = senha
        self.historico = historico if historico is not None else []
    
    def __str__(self):
        return f"[{self.id}] {self.nome} (@{self.username}) | Empréstimos: {len(self.historico)}"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Converte o usuário para dicionário."""
        return {
            'id': self.id,
            'nome': self.nome,
            'username': self.username,
            'senha': self.senha,
            'historico': self.historico
        }
    
    @staticmethod
    def from_dict(data):
        """Cria um usuário a partir de um dicionário."""
        return Usuario(
            id=data['id'],
            nome=data['nome'],
            username=data['username'],
            senha=data['senha'],
            historico=data.get('historico', [])
        )
