"""
Interface principal do sistema de biblioteca.
"""

from src.database import Database

def exibir_menu():
    """Exibe o menu principal."""
    print("\n" + "="*50)
    print("         SISTEMA DE BIBLIOTECA")
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
    print("0. Sair")
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

def emprestar_livro(db):
    """Marca um livro como emprestado."""
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
        print(f"\n✓ Livro '{livro.titulo}' emprestado com sucesso!")
    except ValueError:
        print("\n✗ Erro: ID deve ser um número!")

def devolver_livro(db):
    """Marca um livro como devolvido."""
    try:
        livro_id = int(input("\nID do livro a devolver: "))
        livro = db.buscar_por_id(livro_id)
        if not livro:
            print(f"\n✗ Livro com ID {livro_id} não encontrado!")
            return
        
        if livro.disponivel:
            print(f"\n✗ O livro '{livro.titulo}' já está disponível!")
            return
        
        db.devolver(livro_id)
        print(f"\n✓ Livro '{livro.titulo}' devolvido com sucesso!")
    except ValueError:
        print("\n✗ Erro: ID deve ser um número!")

def main():
    """Função principal."""
    db = Database()
    
    while True:
        exibir_menu()
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
                emprestar_livro(db)
            elif opcao == "10":
                devolver_livro(db)
            elif opcao == "0":
                print("\nAté logo!")
                break
            else:
                print("\n✗ Opção inválida! Tente novamente.")
        except Exception as e:
            print(f"\n✗ Erro inesperado: {e}")

if __name__ == "__main__":
    main()
