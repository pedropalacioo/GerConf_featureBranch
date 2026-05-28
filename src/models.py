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
