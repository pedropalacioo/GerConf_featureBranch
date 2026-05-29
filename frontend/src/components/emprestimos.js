const STORAGE_LIVROS = 'bibbleteca_livros';
const STORAGE_EMPRESTIMOS = 'bibbleteca_emprestimos';

function getLivros() {
  return JSON.parse(localStorage.getItem(STORAGE_LIVROS)) || [];
}

function salvarLivros(livros) {
  localStorage.setItem(STORAGE_LIVROS, JSON.stringify(livros));
}

function getEmprestimos() {
  return JSON.parse(localStorage.getItem(STORAGE_EMPRESTIMOS)) || [];
}

function salvarEmprestimos(emprestimos) {
  localStorage.setItem(STORAGE_EMPRESTIMOS, JSON.stringify(emprestimos));
}

export function renderEmprestimos() {
  return `
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h1 class="dashboard-title bibble-text">
          Empréstimos
        </h1>
        <p class="dashboard-subtitle">Gira os empréstimos e as devoluções da tua biblioteca mágica.</p>
      </div>
      
      <div class="actions-bar">
        <div class="search-box">
          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
          <input type="text" placeholder="Procurar um empréstimo..." class="bibble-input with-icon" id="search-emprestimo">
        </div>
        
        <button class="btn-bibble" id="btn-add-emprestimo" style="display: flex; align-items: center; gap: 8px;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
          Novo Empréstimo
        </button>
      </div>

      <div class="books-grid" id="emprestimos-list"></div>
    </div>

    <div id="modal-add-emprestimo" class="modal-overlay hidden">
      <div class="modal-content bibble-card">
        <h2 class="bibble-text" style="margin-bottom: 20px; display: flex; align-items: center; justify-content: center; gap: 10px;">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="12" y1="18" x2="12" y2="12"></line><line x1="9" y1="15" x2="15" y2="15"></line></svg>
          Registar Empréstimo
        </h2>
        <form id="form-add-emprestimo" class="bibble-form">
          <select id="select-livro" class="bibble-input full-width" required>
            <option value="" disabled selected>Escolhe um livro disponível...</option>
          </select>
          <input type="text" id="input-leitor" class="bibble-input full-width" placeholder="Nome do Leitor" required>
          <div class="modal-actions">
            <button type="button" class="btn-bibble btn-cancel" id="btn-cancel-add-emp">Cancelar</button>
            <button type="submit" class="btn-bibble">Emprestar</button>
          </div>
        </form>
      </div>
    </div>

    <div id="modal-return-emprestimo" class="modal-overlay hidden">
      <div class="modal-content bibble-card">
        <h2 class="bibble-text" style="margin-bottom: 15px; display: flex; align-items: center; justify-content: center; gap: 10px; color: var(--bibble-blue);">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--bibble-blue)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 11 12 14 22 4"></polyline><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path></svg>
          Devolver Livro
        </h2>
        <p style="margin-bottom: 25px; color: #64748b; font-size: 15px;">
          Confirma a devolução do livro <strong id="return-book-title" style="color: var(--text-main);"></strong>?
        </p>
        <div class="modal-actions">
          <button type="button" class="btn-bibble btn-cancel" id="btn-cancel-return">Cancelar</button>
          <button type="button" class="btn-bibble" id="btn-confirm-return" style="background: linear-gradient(135deg, var(--bibble-blue), #3b82f6);">Confirmar</button>
        </div>
      </div>
    </div>
  `;
}

export function initEmprestimos() {
  const container = document.getElementById('emprestimos-list');
  const btnAdd = document.getElementById('btn-add-emprestimo');
  
  const modalAdd = document.getElementById('modal-add-emprestimo');
  const btnCancelAdd = document.getElementById('btn-cancel-add-emp');
  const formAdd = document.getElementById('form-add-emprestimo');
  const selectLivro = document.getElementById('select-livro');

  const modalReturn = document.getElementById('modal-return-emprestimo');
  const btnCancelReturn = document.getElementById('btn-cancel-return');
  const btnConfirmReturn = document.getElementById('btn-confirm-return');
  const returnBookTitle = document.getElementById('return-book-title');
  
  let emprestimoIdParaDevolver = null;

  function atualizarListaLivrosDisponiveis() {
    const livros = getLivros();
    const livrosDisponiveis = livros.filter(l => l.disponivel);
    
    selectLivro.innerHTML = '<option value="" disabled selected>Escolhe um livro disponível...</option>';
    
    if (livrosDisponiveis.length === 0) {
      selectLivro.innerHTML += '<option value="" disabled>Nenhum livro disponível no momento</option>';
    } else {
      livrosDisponiveis.forEach(livro => {
        selectLivro.innerHTML += `<option value="${livro.id}">${livro.titulo} (ID: ${livro.id})</option>`;
      });
    }
  }

  function renderEmprestimos() {
    let emprestimos = getEmprestimos();
    
    const ativos = emprestimos.filter(emp => emp.status === 'ativo');

    if (ativos.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
          <img src="/bibble-image.jpeg" alt="Bibble segurando um livro" style="width: 220px; border-radius: 24px; box-shadow: 0 12px 25px rgba(142, 68, 173, 0.25); margin-bottom: 24px; transform: rotate(2deg);">
          <p style="color: var(--bibble-purple); font-size: 24px; font-weight: 700; margin-bottom: 8px;">Nenhum empréstimo ativo</p>
          <p style="color: #64748b; font-size: 16px;">Os livros estão todos seguros na prateleira da Bibbleteca.</p>
        </div>
      `;
      return;
    }

    container.innerHTML = ativos.map(emp => `
      <div class="book-card bibble-card" data-id="${emp.id}">
        <div class="book-status status-unavailable">
          Emprestado
        </div>
        <div class="book-icon" style="margin-bottom: 15px;">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--barbie-pink)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.828 2.828 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"></path></svg>
        </div>
        <h3 class="book-title" style="margin-bottom: 10px;">${emp.livroTitulo}</h3>
        <p class="book-author" style="font-weight: 600; color: var(--bibble-purple); margin-bottom: 5px;">Leitor: ${emp.leitor}</p>
        <p class="book-author" style="font-size: 12px;">Data: ${emp.dataEmprestimo}</p>
        
        <div class="card-actions" style="margin-top: 15px;">
          <button class="btn-bibble btn-return" style="width: 100%; padding: 8px; font-size: 14px; background: linear-gradient(135deg, var(--bibble-blue-light), white); color: var(--bibble-blue); border: 2px solid var(--bibble-blue);" title="Devolver livro">
            Devolver Livro
          </button>
        </div>
      </div>
    `).join('');

    document.querySelectorAll('.btn-return').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const card = e.target.closest('.book-card');
        emprestimoIdParaDevolver = Number(card.dataset.id);
        const emprestimosAtuais = getEmprestimos();
        const emprestimoToReturn = emprestimosAtuais.find(e => e.id === emprestimoIdParaDevolver);
        
        returnBookTitle.textContent = `"${emprestimoToReturn.livroTitulo}"`;
        modalReturn.classList.remove('hidden');
      });
    });
  }

  renderEmprestimos();

  btnAdd.addEventListener('click', () => {
    atualizarListaLivrosDisponiveis();
    formAdd.reset();
    modalAdd.classList.remove('hidden');
  });

  btnCancelAdd.addEventListener('click', () => {
    modalAdd.classList.add('hidden');
    formAdd.reset();
  });

  formAdd.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const livroIdSelecionado = Number(selectLivro.value);
    const leitor = document.getElementById('input-leitor').value;
    
    if (!livroIdSelecionado) return;

    let livros = getLivros();
    let emprestimos = getEmprestimos();

    const livroIndex = livros.findIndex(l => l.id === livroIdSelecionado);
    if (livroIndex !== -1) {
      livros[livroIndex].disponivel = false;
      salvarLivros(livros);
      
      const dataAtual = new Date().toLocaleDateString('pt-PT');
      const novoEmprestimo = {
        id: Date.now(),
        livroId: livroIdSelecionado,
        livroTitulo: livros[livroIndex].titulo,
        leitor: leitor,
        dataEmprestimo: dataAtual,
        status: 'ativo'
      };
      
      emprestimos.push(novoEmprestimo);
      salvarEmprestimos(emprestimos);
    }

    renderEmprestimos();
    modalAdd.classList.add('hidden');
    formAdd.reset();
  });

  btnCancelReturn.addEventListener('click', () => {
    modalReturn.classList.add('hidden');
    emprestimoIdParaDevolver = null;
  });

  btnConfirmReturn.addEventListener('click', () => {
    if (emprestimoIdParaDevolver) {
      let emprestimos = getEmprestimos();
      let livros = getLivros();

      const empIndex = emprestimos.findIndex(e => e.id === emprestimoIdParaDevolver);
      
      if (empIndex !== -1) {
        const idDoLivro = emprestimos[empIndex].livroId;
        
        emprestimos[empIndex].status = 'devolvido';
        emprestimos[empIndex].dataDevolucao = new Date().toLocaleDateString('pt-PT');
        
        const livroIndex = livros.findIndex(l => l.id === idDoLivro);
        if (livroIndex !== -1) {
          livros[livroIndex].disponivel = true;
        }

        salvarEmprestimos(emprestimos);
        salvarLivros(livros);
        
        renderEmprestimos();
      }
      
      modalReturn.classList.add('hidden');
      emprestimoIdParaDevolver = null;
    }
  });
}
