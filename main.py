"""
Interface principal do sistema de biblioteca.
"""

from src.database import Database, UsuarioDatabase

def exibir_menu_login():
    """Exibe o menu de login."""
    print("\n" + "="*50)
    print("         SISTEMA DE BIBLIOTECA - LOGIN")
    print("="*50)
    print("1. Fazer Login")
    print("2. Cadastrar Novo Usuário")
    print("0. Sair")
    print("="*50)

def login(db_usuarios):
    """Realiza o login do usuário."""
    print("\n--- Login ---")
    username = input("Username: ").strip()
    senha = input("Senha: ").strip()
    
    usuario = db_usuarios.autenticar(username, senha)
    if usuario:
        print(f"\n✓ Bem-vindo, {usuario.nome}!")
        return usuario
    else:
        print("\n✗ Usuário ou senha incorretos!")
        return None

def cadastrar_usuario(db_usuarios):
    """Cadastra um novo usuário."""
    print("\n--- Cadastro de Usuário ---")
    nome = input("Nome completo: ").strip()
    username = input("Username: ").strip()
    senha = input("Senha: ").strip()
    
    if nome and username and senha:
        usuario = db_usuarios.criar_usuario(nome, username, senha)
        if usuario:
            print(f"\n✓ Usuário '{username}' cadastrado com sucesso!")
        else:
            print("\n✗ Erro: Username já existe!")
    else:
        print("\n✗ Erro: Todos os campos são obrigatórios!")

def ver_historico(usuario):
    """Exibe o histórico de empréstimos do usuário logado."""
    print(f"\n--- Histórico de {usuario.nome} ---")
    if not usuario.historico:
        print("Nenhum registro encontrado.")
    else:
        for item in usuario.historico:
            status = "✓ Devolvido" if item['status'] == 'devolvido' else "⚠ Pendente"
            print(f"- {item['titulo']} | Status: {status}")

def exibir_menu(usuario):
    """Exibe o menu principal."""
    print("\n" + "="*50)
    print(f"         SISTEMA DE BIBLIOTECA (Logado: {usuario.username})")
    print("="*50)
    print("1. Adicionar novo livro")
    print("2. Listar todos os livros")
    print("3. Listar livros disponíveis")
    print("4. Buscar livro por ID")
    print("5. Buscar livro por título")
    print("6. Buscar livro por autor")
    print("7. Atualizar livro")
    print("8. Deletar livro")
    print("9. Emprestar livro")
    print("10. Devolver livro")
    print("11. Ver Meu Histórico")
    print("0. Logout")
    print("="*50)

def adicionar_livro(db):
    """Adiciona um novo livro."""
    print("\n--- Adicionar Novo Livro ---")
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    ano = input("Ano de publicação: ").strip()
    genero = input("Gênero: ").strip()
    
    if titulo and autor and ano and genero:
        livro = db.criar(titulo, autor, int(ano), genero)
        print(f"\n✓ Livro adicionado com sucesso!\n{livro}")
    else:
        print("\n✗ Erro: Todos os campos são obrigatórios!")

def listar_livros(db):
    """Lista todos os livros."""
    livros = db.listar()
    if livros:
        print("\n--- Todos os Livros ---")
        for livro in livros:
            print(livro)
    else:
        print("\n✗ Nenhum livro cadastrado!")

def listar_disponiveis(db):
    """Lista livros disponíveis."""
    livros = db.listar_disponiveis()
    if livros:
        print("\n--- Livros Disponíveis ---")
        for livro in livros:
            print(livro)
    else:
        print("\n✗ Nenhum livro disponível no momento!")

def buscar_por_id(db):
    """Busca livro por ID."""
    try:
        livro_id = int(input("\nID do livro: "))
        livro = db.buscar_por_id(livro_id)
        if livro:
            print(f"\n--- Resultado ---\n{livro}")
        else:
            print(f"\n✗ Livro com ID {livro_id} não encontrado!")
    except ValueError:
        print("\n✗ Erro: ID deve ser um número!")

def buscar_por_titulo(db):
    """Busca livro por título."""
    titulo = input("\nTítulo (ou parte dele): ").strip()
    livros = db.buscar_por_titulo(titulo)
    if livros:
        print(f"\n--- Resultados para '{titulo}' ---")
        for livro in livros:
            print(livro)
    else:
        print(f"\n✗ Nenhum livro encontrado com '{titulo}'!")

def buscar_por_autor(db):
    """Busca livro por autor."""
    autor = input("\nAutor (ou parte do nome): ").strip()
    livros = db.buscar_por_autor(autor)
    if livros:
        print(f"\n--- Resultados para '{autor}' ---")
        for livro in livros:
            print(livro)
    else:
        print(f"\n✗ Nenhum livro encontrado de '{autor}'!")

def atualizar_livro(db):
    """Atualiza um livro."""
    try:
        livro_id = int(input("\nID do livro a atualizar: "))
        livro = db.buscar_por_id(livro_id)
        if not livro:
            print(f"\n✗ Livro com ID {livro_id} não encontrado!")
            return
        
        print(f"\nLivro atual: {livro}")
        print("\nDeixe em branco para não alterar um campo.")
        
        titulo = input("Novo título: ").strip() or None
        autor = input("Novo autor: ").strip() or None
        ano = input("Novo ano: ").strip()
        ano = int(ano) if ano else None
        genero = input("Novo gênero: ").strip() or None
        
        livro_atualizado = db.atualizar(livro_id, titulo, autor, ano, genero)
        print(f"\n✓ Livro atualizado!\n{livro_atualizado}")
    except ValueError:
        print("\n✗ Erro: Valores inválidos!")

def deletar_livro(db):
    """Deleta um livro."""
    try:
        livro_id = int(input("\nID do livro a deletar: "))
        livro = db.buscar_por_id(livro_id)
        if not livro:
            print(f"\n✗ Livro com ID {livro_id} não encontrado!")
            return
        
        confirmacao = input(f"Confirmar exclusão de '{livro.titulo}'? (s/n): ").lower()
        if confirmacao == 's':
            db.deletar(livro_id)
            print("\n✓ Livro deletado com sucesso!")
        else:
            print("\n✗ Operação cancelada!")
    except ValueError:
        print("\n✗ Erro: ID deve ser um número!")

def emprestar_livro(db, db_usuarios, usuario_logado):
    """Marca um livro como emprestado e registra no histórico."""
    try:
        livro_id = int(input("\nID do livro a emprestar: "))
        livro = db.buscar_por_id(livro_id)
        if not livro:
            print(f"\n✗ Livro com ID {livro_id} não encontrado!")
            return
        
        if not livro.disponivel:
            print(f"\n✗ O livro '{livro.titulo}' já está emprestado!")
            return
        
        db.emprestar(livro_id)
        db_usuarios.registrar_emprestimo(usuario_logado.id, livro)
        # Atualiza o objeto usuario_logado na memória para refletir o histórico atualizado
        usuario_logado.historico.append({'livro_id': livro.id, 'titulo': livro.titulo, 'status': 'pendente'})
        
        print(f"\n✓ Livro '{livro.titulo}' emprestado com sucesso!")
    except ValueError:
        print("\n✗ Erro: ID deve ser um número!")

def devolver_livro(db, db_usuarios, usuario_logado):
    """Marca um livro como devolvido e atualiza o histórico."""
    try:
        livro_id = int(input("\nID do livro a devolver: "))
        livro = db.buscar_por_id(livro_id)
        if not livro:
            print(f"\n✗ Livro com ID {livro_id} não encontrado!")
            return
        
        if livro.disponivel:
            print(f"\n✗ O livro '{livro.titulo}' já está disponível!")
            return
        
        # Verifica se o livro está no histórico do usuário logado como pendente
        tem_no_historico = False
        for item in usuario_logado.historico:
            if item['livro_id'] == livro_id and item['status'] == 'pendente':
                tem_no_historico = True
                break
        
        if not tem_no_historico:
            print("\n✗ Você não possui este livro em seu histórico de pendências!")
            return

        db.devolver(livro_id)
        db_usuarios.registrar_devolucao(usuario_logado.id, livro_id)
        # Atualiza na memória
        for item in usuario_logado.historico:
            if item['livro_id'] == livro_id and item['status'] == 'pendente':
                item['status'] = 'devolvido'
                break

        print(f"\n✓ Livro '{livro.titulo}' devolvido com sucesso!")
    except ValueError:
        print("\n✗ Erro: ID deve ser um número!")

def main():
    """Função principal com fluxo de login."""
    db = Database()
    db_usuarios = UsuarioDatabase()
    usuario_logado = None
    
    while True:
        if not usuario_logado:
            exibir_menu_login()
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                usuario_logado = login(db_usuarios)
            elif opcao == "2":
                cadastrar_usuario(db_usuarios)
            elif opcao == "0":
                print("\nAté logo!")
                break
            else:
                print("\n✗ Opção inválida!")
        else:
            exibir_menu(usuario_logado)
            opcao = input("Escolha uma opção: ").strip()
            
            try:
                if opcao == "1":
                    adicionar_livro(db)
                elif opcao == "2":
                    listar_livros(db)
                elif opcao == "3":
                    listar_disponiveis(db)
                elif opcao == "4":
                    buscar_por_id(db)
                elif opcao == "5":
                    buscar_por_titulo(db)
                elif opcao == "6":
                    buscar_por_autor(db)
                elif opcao == "7":
                    atualizar_livro(db)
                elif opcao == "8":
                    deletar_livro(db)
                elif opcao == "9":
                    emprestar_livro(db, db_usuarios, usuario_logado)
                elif opcao == "10":
                    devolver_livro(db, db_usuarios, usuario_logado)
                elif opcao == "11":
                    ver_historico(usuario_logado)
                elif opcao == "0":
                    print(f"\nLogout realizado: {usuario_logado.username}")
                    usuario_logado = None
                else:
                    print("\n✗ Opção inválida! Tente novamente.")
            except Exception as e:
                print(f"\n✗ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
