// Chave para guardar no LocalStorage
const STORAGE_KEY = 'bibbleteca_livros';

// Tenta carregar os livros guardados ou começa com uma lista vazia
let livros = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];

// Função auxiliar para guardar no LocalStorage sempre que houver mudanças
function salvarNoStorage() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(livros));
}

export function renderGerirLivros() {
  return /*html*/`
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h1 class="dashboard-title bibble-text">
          Gerir Livros
        </h1>
        <p class="dashboard-subtitle">Adicione, edite ou remova os livros da biblioteca.</p>
      </div>
      
      <div class="actions-bar">
        <!-- Campo de Pesquisa com Lupa -->
        <div class="search-box">
          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" placeholder="Procurar um livro..." class="bibble-input with-icon" id="search-livro">
        </div>
        
        <button class="btn-bibble" id="btn-add-livro" style="display: flex; align-items: center; gap: 8px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
          Adicionar Novo Livro
        </button>
      </div>

      <div class="books-grid" id="books-list"></div>
    </div>

    <!-- Modal de Cadastro/Edição de Livro -->
    <div id="modal-add-livro" class="modal-overlay hidden">
      <div class="modal-content bibble-card">
        <h2 id="modal-add-title" class="bibble-text" style="margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 10px;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
          Novo Livro
        </h2>
        <form id="form-add-livro" class="bibble-form">
          <input type="text" id="input-titulo" class="bibble-input full-width" placeholder="Título do Livro" required>
          <input type="text" id="input-autor" class="bibble-input full-width" placeholder="Autor" required>
          <input type="text" id="input-genero" class="bibble-input full-width" placeholder="Gênero (ex: Fantasia)" required>
          <input type="number" id="input-ano" class="bibble-input full-width" placeholder="Ano de Publicação" required>
          
          <div class="modal-actions">
            <button type="button" class="btn-bibble btn-cancel" id="btn-cancel-add">Cancelar</button>
            <button type="submit" class="btn-bibble">Salvar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal de Confirmação de Exclusão -->
    <div id="modal-delete-livro" class="modal-overlay hidden">
      <div class="modal-content bibble-card">
        <h2 class="bibble-text" style="margin-bottom: 15px; display: flex; align-items: center; justify-content: center; gap: 10px; color: #ef4444;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
          Excluir Livro
        </h2>
        <p style="margin-bottom: 25px; color: #64748b; font-size: 15px;">
          Tem certeza que deseja apagar o livro <strong id="delete-book-title" style="color: var(--text-main);"></strong>? Esta ação não pode ser desfeita.
        </p>
        <div class="modal-actions">
          <button type="button" class="btn-bibble btn-cancel" id="btn-cancel-delete">Cancelar</button>
          <button type="button" class="btn-bibble btn-danger" id="btn-confirm-delete">Excluir</button>
        </div>
      </div>
    </div>
  `;
}

export function initGerirLivros() {
  const container = document.getElementById('books-list');
  const btnAdd = document.getElementById('btn-add-livro');
  
  // Elementos do Modal de Adicionar/Editar
  const modalAdd = document.getElementById('modal-add-livro');
  const btnCancelAdd = document.getElementById('btn-cancel-add');
  const formAdd = document.getElementById('form-add-livro');
  const modalAddTitle = document.getElementById('modal-add-title');
  
  // Variável para controlar se estamos a editar ou a criar
  let livroIdSendoEditado = null;

  // Elementos do Modal de Exclusão
  const modalDelete = document.getElementById('modal-delete-livro');
  const btnCancelDelete = document.getElementById('btn-cancel-delete');
  const btnConfirmDelete = document.getElementById('btn-confirm-delete');
  const deleteBookTitle = document.getElementById('delete-book-title');
  let livroIdParaExcluir = null;

  function renderBooks() {
    if (livros.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <img src="/bibble-image.jpeg" alt="Bibble segurando um livro mágico" style="width: 220px; border-radius: 24px; box-shadow: 0 12px 25px rgba(142, 68, 173, 0.25); margin-bottom: 24px; transform: rotate(-2deg);">
          <p style="color: var(--bibble-purple); font-size: 24px; font-weight: 700; margin-bottom: 8px;">A tua Bibbleteca está vazia! </p>
          <p style="color: #64748b; font-size: 16px;">Adiciona o teu primeiro conto de fadas clicando no botão acima.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = livros.map(book => /*html*/`
      <div class="book-card bibble-card" data-id="${book.id}">
        <div class="book-status ${book.disponivel ? 'status-available' : 'status-unavailable'}">
          ${book.disponivel ? 'Disponível' : 'Emprestado'}
        </div>
        <div class="book-icon" style="margin-bottom: 15px;">
          ${book.disponivel 
            ? '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--bibble-blue)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>'
            : '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--barbie-pink)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>'}
        </div>
        <h3 class="book-title">${book.titulo}</h3>
        <p class="book-author">${book.autor}</p>
        <div class="book-tags">
          <span class="tag tag-blue">${book.genero}</span>
          <span class="tag tag-purple">${book.ano}</span>
        </div>
        <div class="card-actions">
          <button class="btn-icon edit" title="Editar livro">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
          </button>
          <button class="btn-icon delete" title="Eliminar livro">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
          </button>
        </div>
      </div>
    `).join('');

    // Lógica para ABRIR modal de edição
    document.querySelectorAll('.btn-icon.edit').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const card = e.target.closest('.book-card');
        livroIdSendoEditado = Number(card.dataset.id);
        const bookToEdit = livros.find(l => l.id === livroIdSendoEditado);
        
        // Preenche o formulário com os dados do livro
        document.getElementById('input-titulo').value = bookToEdit.titulo;
        document.getElementById('input-autor').value = bookToEdit.autor;
        document.getElementById('input-genero').value = bookToEdit.genero;
        document.getElementById('input-ano').value = bookToEdit.ano;
        
        // Atualiza o título do modal
        modalAddTitle.innerHTML = `
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
          Editar Livro
        `;
        
        modalAdd.classList.remove('hidden');
      });
    });

    // Lógica para ABRIR modal de exclusão
    document.querySelectorAll('.btn-icon.delete').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const card = e.target.closest('.book-card');
        livroIdParaExcluir = Number(card.dataset.id);
        const bookToDelete = livros.find(l => l.id === livroIdParaExcluir);
        
        deleteBookTitle.textContent = `"${bookToDelete.titulo}"`;
        modalDelete.classList.remove('hidden');
      });
    });
  }

  // Inicializa a tela com os dados do localStorage
  renderBooks();

  // ----- EVENTOS MODAL ADICIONAR / EDITAR -----
  btnAdd.addEventListener('click', () => {
    // Reseta a variável de edição e limpa o form
    livroIdSendoEditado = null;
    formAdd.reset();
    
    // Volta ao título padrão
    modalAddTitle.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path></svg>
      Novo Livro
    `;
    
    modalAdd.classList.remove('hidden');
  });

  btnCancelAdd.addEventListener('click', () => {
    modalAdd.classList.add('hidden');
    formAdd.reset();
    livroIdSendoEditado = null;
  });

  formAdd.addEventListener('submit', (e) => {
    e.preventDefault();
    
    if (livroIdSendoEditado) {
      // Se tivermos um ID, estamos a editar o livro
      const index = livros.findIndex(l => l.id === livroIdSendoEditado);
      if (index !== -1) {
        livros[index].titulo = document.getElementById('input-titulo').value;
        livros[index].autor = document.getElementById('input-autor').value;
        livros[index].genero = document.getElementById('input-genero').value;
        livros[index].ano = parseInt(document.getElementById('input-ano').value);
      }
    } else {
      // Se não, criamos um novo livro
      const novoLivro = {
        id: Date.now(),
        titulo: document.getElementById('input-titulo').value,
        autor: document.getElementById('input-autor').value,
        genero: document.getElementById('input-genero').value,
        ano: parseInt(document.getElementById('input-ano').value),
        disponivel: true
      };
      livros.push(novoLivro);
    }

    salvarNoStorage(); // Salva no LocalStorage
    renderBooks();    // Atualiza a tela
    
    modalAdd.classList.add('hidden');
    formAdd.reset();
    livroIdSendoEditado = null; // Reseta para a próxima ação
  });

  // ----- EVENTOS MODAL EXCLUSÃO -----
  btnCancelDelete.addEventListener('click', () => {
    modalDelete.classList.add('hidden');
    livroIdParaExcluir = null;
  });

  btnConfirmDelete.addEventListener('click', () => {
    if (livroIdParaExcluir) {
      livros = livros.filter(l => l.id !== livroIdParaExcluir);
      salvarNoStorage(); // Atualiza o LocalStorage após remover
      renderBooks();     // Atualiza a tela
      
      modalDelete.classList.add('hidden');
      livroIdParaExcluir = null;
    }
  });
}