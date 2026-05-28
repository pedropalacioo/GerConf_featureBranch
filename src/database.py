"""
Gerenciamento de banco de dados para livros, reservas, categorias e relatórios.
"""

import json
import os
from datetime import datetime, date
from models import Livro

class Database:
    """Gerencia o armazenamento, recuperação e relatórios do sistema de biblioteca."""
    
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
    
    # ==================== CRUD & CATEGORIAS ====================
    
    def criar(self, titulo, autor, ano, genero, categoria="Geral"):
        """Cria um novo livro adicionando o conceito de Categoria."""
        livros = self._carregar()
        novo_id = self._proxima_id()
        novo_livro = Livro(
            id=novo_id,
            titulo=titulo,
            autor=autor,
            ano=ano,
            genero=genero
        )
        
        novo_livro.categoria = categoria 
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

    def buscar_por_categoria(self, categoria):
        """Filtra livros por uma categoria específica (Ex: 'Acadêmico', 'Infantil')."""
        livros = self._carregar()
        return [livro for livro in livros if categoria.lower() in getattr(livro, 'categoria', '').lower()]
    
    def buscar_por_titulo(self, titulo):
        """Busca livros pelo título."""
        livros = self._carregar()
        return [livro for livro in livros if titulo.lower() in livro.titulo.lower()]
    
    def buscar_por_autor(self, autor):
        """Busca livros pelo autor."""
        livros = self._carregar()
        return [livro for livro in livros if autor.lower() in livro.autor.lower()]
    
    def atualizar(self, livro_id, titulo=None, autor=None, ano=None, genero=None, disponivel=None, reservado_por=None, categoria=None, data_devolucao_prevista=None):
        """Atualiza os dados cadastrais e estados de controle do livro."""
        livros = self._carregar()
        for livro in livros:
            if livro.id == livro_id:
                if titulo is not None: livro.titulo = titulo
                if autor is not None: livro.autor = autor
                if ano is not None: livro.ano = ano
                if genero is not None: livro.genero = genero
                if disponivel is not None: livro.disponivel = disponivel
                if categoria is not None: livro.categoria = categoria
                if data_devolucao_prevista is not None: livro.data_devolucao_prevista = data_devolucao_prevista
                
                if reservado_por is False:
                    livro.reservado_por = None
                elif reservado_por is not None:
                    livro.reservado_por = reservado_por
                    
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
    
    # ==================== EMPRÉSTIMOS, RESERVAS & MULTAS ====================
    
    def emprestar(self, livro_id, data_limite_iso=None):
        """
        Marca como emprestado e define uma data de devolução prevista (Formato: YYYY-MM-DD).
        Se nenhuma data for passada, herda o padrão de 14 dias a partir de hoje.
        """
        if not data_limite_iso:
            from datetime import timedelta
            data_limite_iso = (date.today() + timedelta(days=14)).isoformat()
            
        return self.atualizar(livro_id, disponivel=False, data_devolucao_prevista=data_limite_iso)
    
    def devolver(self, livro_id):
        """Remove o vínculo de datas de devolução e limpa o status para disponível."""
        return self.atualizar(livro_id, disponivel=True, data_devolucao_prevista=False)

    def reservar(self, livro_id, usuario_id):
        """Reserva um livro caso ele esteja indisponível e sem reservas prévias."""
        livro = self.buscar_por_id(livro_id)
        if livro and not livro.disponivel and not getattr(livro, 'reservado_por', None):
            return self.atualizar(livro_id, reservado_por=usuario_id)
        return None

    def calcular_multa_livro(self, livro):
        """
        Calcula a multa caso o livro esteja atrasado.
        Regra: R$ 0,5 por dia de atraso.
        """
        data_prevista_str = getattr(livro, 'data_devolucao_prevista', None)
        if not data_prevista_str or livro.disponivel:
            return 0.0
        
        try:
            data_prevista = datetime.strptime(data_prevista_str, "%Y-%m-%d").date()
            hoje = date.today()
            if hoje > data_prevista:
                dias_atraso = (hoje - data_prevista).days
                return dias_atraso * 0.5
        except ValueError:
            pass
        return 0.0

    # ==================== SISTEMA DE RELATÓRIOS ====================
    
    def gerar_relatorio_geral(self):
        """Retorna dicionário com métricas agregadas da biblioteca."""
        livros = self._carregar()
        total = len(livros)
        disponiveis = len([l for l in livros if l.disponivel])
        emprestados = total - disponiveis
        reservados = len([l for l in livros if getattr(l, 'reservado_por', None)])
        
        total_multas = 0.0
        livros_atrasados = 0
        for l in livros:
            multa = self.calcular_multa_livro(l)
            if multa > 0:
                total_multas += multa
                livros_atrasados += 1

        return {
            "total_livros": total,
            "quantidade_disponiveis": disponiveis,
            "quantidade_emprestados": emprestados,
            "quantidade_reservados": reservados,
            "livros_em_atraso": livros_atrasados,
            "valor_total_multas_pendentes": total_multas
        }

    def listar_livros_atrasados(self):
        """Retorna uma lista de dicionários contendo livros atrasados e o valor da multa."""
        livros = self._carregar()
        atrasados = []
        for l in livros:
            multa = self.calcular_multa_livro(l)
            if multa > 0:
                atrasados.append({
                    "id": l.id,
                    "titulo": l.titulo,
                    "data_prevista": l.data_devolucao_prevista,
                    "multa_acumulada": multa
                })
        return atrasados