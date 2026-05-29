# Sistema de Biblioteca

Um sistema simples de biblioteca em Python com funcionalidades de CRUD para gerenciar livros.

## Estrutura do Projeto

```
GerConf_featureBranch/
├── frontend/             # Frontend da aplicação com Vite
├── src/
│   ├── __init__.py       # Inicialização do módulo
│   ├── models.py         # Modelo da classe Livro
│   └── database.py       # Gerenciamento de banco de dados
├── data/
│   └── livros.json       # Arquivo de armazenamento (gerado automaticamente)
├── main.py              # Interface principal da aplicação
└── README.md            # Este arquivo
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

### 1. Executar Backend

```bash
python main.py
```

### 2. Inicializar Servidor Frontend

```bash
cd frontend
npm i
npm run dev
```

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

## Dependências

Nenhuma dependência externa! O projeto usa apenas bibliotecas padrão do Python.

## 👥 Equipe e Distribuição de Tarefas

### ✅ Concluído
- **Rayan** - CRUD de Livros (Create, Read, Update, Delete)

### 📋 Em Desenvolvimento

| Pessoa | Responsabilidade |
|--------|-----------------|
| Samuel | 👤 [Sistema de Usuários](./DOCUMENTACAO_USUARIOS.md), Autenticação, Histórico de Empréstimos |
| **Sebastião** | 🎨 Frontend - Estrutura, Layout, Templates Base |
| **Ramon** | 🎨 Frontend - CRUD de Livros (Interface), Empréstimos, Filtros |
| **Sabrina** | 📊 Sistema de Reservas, Multas, Categorias, Relatórios |
| **Pedro** | 🔧 API REST, Testes, Deployment |

Para mais detalhes sobre as tarefas específicas, consulte [DISTRIBUICAO_TAREFAS.md](DISTRIBUICAO_TAREFAS.md).

## Notas

- Os IDs dos livros são gerados automaticamente
- A busca por título e autor é case-insensitive
- O arquivo JSON é formatado para facilitar leitura e edição manual
- Todas as operações preservam a integridade dos dados
