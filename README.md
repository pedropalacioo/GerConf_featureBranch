# Sistema de Biblioteca

Um sistema simples de biblioteca em Python com funcionalidades de CRUD para gerenciar livros.

## Estrutura do Projeto

```
GerConf_featureBranch/
├── src/
│   ├── __init__.py       # Inicialização do módulo
│   ├── models.py         # Modelo da classe Livro
│   └── database.py       # Gerenciamento de banco de dados
├── data/
│   └── livros.json       # Arquivo de armazenamento (gerado automaticamente)
├── main.py               # Interface CLI da aplicação
├── api.py                # API REST com FastAPI
├── test_api.py           # Testes automatizados com pytest
├── requirements.txt      # Dependências do projeto
└── README.md             # Este arquivo
```

## Funcionalidades

### CRUD de Livros
- ✅ **Criar**: Adicionar novos livros à biblioteca
- ✅ **Ler**: Listar todos os livros ou buscar por critérios
- ✅ **Atualizar**: Modificar informações de um livro
- ✅ **Deletar**: Remover livros da biblioteca

### Buscas
- Buscar por ID
- Buscar por título (busca parcial)
- Buscar por autor (busca parcial)

### Gerenciamento de Disponibilidade
- Listar apenas livros disponíveis
- Emprestar livro (marca como indisponível)
- Devolver livro (marca como disponível)

## Como Usar

### Opção 1: Interface CLI (Menu Interativo)

```bash
python main.py
```

### Opção 2: API REST com FastAPI (Recomendado)

```bash
uvicorn api:app --reload
```

A API estará disponível em:
- 🌐 **API Base**: `http://localhost:8000`
- 📚 **Documentação Interativa**: `http://localhost:8000/docs`
- 🔧 **ReDoc**: `http://localhost:8000/redoc`

### Menu Principal (CLI)

A aplicação exibe um menu interativo com as seguintes opções:

```
1. Adicionar novo livro
2. Listar todos os livros
3. Listar livros disponíveis
4. Buscar livro por ID
5. Buscar livro por título
6. Buscar livro por autor
7. Atualizar livro
8. Deletar livro
9. Emprestar livro
10. Devolver livro
0. Sair
```

### 3. Exemplos de Uso

**Adicionar um livro:**
```
1 (Enter)
Título: 1984
Autor: George Orwell
Ano de publicação: 1949
Gênero: Ficção Científica
```

**Listar todos os livros:**
```
2 (Enter)
```

**Buscar por autor:**
```
6 (Enter)
Autor (ou parte do nome): Orwell
```

## API REST - Endpoints

### Health Check
```http
GET /
```

### Livros
```http
GET    /livros                  # Listar todos os livros
POST   /livros                  # Criar novo livro
GET    /livros/{id}             # Obter livro por ID
PUT    /livros/{id}             # Atualizar livro
DELETE /livros/{id}             # Deletar livro
```

### Filtros e Buscas
```http
GET /livros/disponiveis         # Listar apenas livros disponíveis
GET /livros/busca/titulo?q=    # Buscar por título
GET /livros/busca/autor?q=     # Buscar por autor
```

### Empréstimos
```http
POST /livros/{id}/emprestar     # Emprestar livro
POST /livros/{id}/devolver      # Devolver livro
```

### Exemplos de Requisição (curl)

**Criar um livro:**
```bash
curl -X POST http://localhost:8000/livros \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "1984",
    "autor": "George Orwell",
    "ano": 1949,
    "genero": "Ficção Científica"
  }'
```

**Listar todos os livros:**
```bash
curl http://localhost:8000/livros
```

**Emprestar um livro:**
```bash
curl -X POST http://localhost:8000/livros/1/emprestar
```

## Testes

### Executar Todos os Testes

```bash
pytest test_api.py -v
```

### Executar com Mais Detalhes

```bash
pytest test_api.py -v --tb=short
```

### Executar Teste Específico

```bash
pytest test_api.py::test_api_criar_livro -v
```

### Cobertura de Testes

O arquivo `test_api.py` contém **26 testes** cobrindo:
- ✅ Modelos (Livro)
- ✅ Database (CRUD, Buscas, Disponibilidade)
- ✅ API REST (Todos os endpoints)

## Estrutura de Dados

### Modelo Livro

```python
{
  "id": 1,
  "titulo": "1984",
  "autor": "George Orwell",
  "ano": 1949,
  "genero": "Ficção Científica",
  "disponivel": true
}
```

## Armazenamento

Os livros são armazenados em formato JSON no arquivo `data/livros.json`. O arquivo é criado automaticamente na primeira execução.

## Requisitos

- Python 3.6+
- pip (gerenciador de pacotes Python)

## Instalação

### 1. Clonar o Repositório

```bash
git clone <repository-url>
cd GerConf_featureBranch
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### Dependências

- **FastAPI** - Framework moderno para criar APIs REST
- **uvicorn** - Servidor ASGI para executar a API
- **pydantic** - Validação de dados com type hints
- **pytest** - Framework para testes automatizados

## 👥 Equipe e Distribuição de Tarefas

### ✅ Concluído
- **Rayan** - CRUD de Livros (Create, Read, Update, Delete)
- **Pedro** - ✅ API REST (FastAPI), ✅ Testes (pytest)

### 📋 Em Desenvolvimento

| Pessoa | Responsabilidade | Status |
|--------|-----------------|--------|
| **Samuel** | 👤 Sistema de Usuários, Autenticação, Histórico de Empréstimos | 📋 |
| **Sebastião** | 🎨 Frontend - Estrutura, Layout, Templates Base | 📋 |
| **Ramon** | 🎨 Frontend - CRUD de Livros (Interface), Empréstimos, Filtros | 📋 |
| **Sabrina** | 📊 Sistema de Reservas, Multas, Categorias, Relatórios | 📋 |
| **Pedro** | 🔧 API REST, Testes, ✅ Deployment | ⏳ |

Para mais detalhes sobre as tarefas específicas, consulte [DISTRIBUICAO_TAREFAS.md](DISTRIBUICAO_TAREFAS.md).

## Notas

- Os IDs dos livros são gerados automaticamente
- A busca por título e autor é case-insensitive
- O arquivo JSON é formatado para facilitar leitura e edição manual
- Todas as operações preservam a integridade dos dados
- A API REST possui CORS habilitado para integração com frontend
- Os testes usam banco de dados temporário (não afetam dados reais)

## Troubleshooting

### Porta 8000 já em uso
```bash
uvicorn api:app --reload --port 8001
```

### Erro ao instalar dependências
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Desenvolvimento Futuro

- 📦 **Deployment**: Docker, CI/CD
- 🗄️ **Banco de Dados**: Migrar de JSON para SQLite/PostgreSQL
- 🔐 **Autenticação**: JWT tokens
- 📱 **Frontend**: Integração com React/Vue