# Documentação do Sistema de Usuários

Esta documentação detalha como integrar e utilizar o sistema de usuários, autenticação e histórico desenvolvido para o Sistema de Biblioteca.

## 🏗️ Estrutura de Classes

### 1. `Usuario` (em `src/models.py`)

Representa a entidade do usuário.

- **Atributos:**
  - `id` (int): Identificador único.
  - `nome` (str): Nome completo.
  - `username` (str): Nome de usuário para login.
  - `senha` (str): Senha em texto plano.
  - `historico` (list): Lista de dicionários contendo os empréstimos.

- **Exemplo de item no histórico:**

    ```python
    {
      "livro_id": 1,
      "titulo": "1984",
      "status": "pendente" # ou "devolvido"
    }
    ```

### 2. `UsuarioDatabase` (em `src/database.py`)

Gerencia a persistência no arquivo `data/usuarios.json`.

- **`criar_usuario(nome, username, senha)`**: Cria e salva um novo usuário. Retorna o objeto `Usuario` ou `None` se o username já existir.
- **`autenticar(username, senha)`**: Verifica as credenciais. Retorna o objeto `Usuario` se bem-sucedido, caso contrário `None`.
- **`registrar_emprestimo(usuario_id, livro_objeto)`**: Adiciona o livro ao histórico do usuário como "pendente".
- **`registrar_devolucao(usuario_id, livro_id)`**: Altera o status do livro no histórico para "devolvido".

---

## 🎨 Guia para Integração com Frontend

Para os desenvolvedores de interface (Sebastião e Ramon), o fluxo de uso deve ser:

1. **Instanciação:**

    ```python
    from src.database import UsuarioDatabase
    db_user = UsuarioDatabase()
    ```

2. **Sessão:** Manter uma variável global ou de estado (ex: `usuario_logado`) após o sucesso do método `db_user.autenticar()`.
3. **Exibição:** O histórico pode ser iterado diretamente de `usuario_logado.historico`.
