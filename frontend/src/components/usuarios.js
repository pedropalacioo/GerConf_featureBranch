export function renderUsuarios() {
  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Gerenciamento de Usuários</h1>
          <p class="page-subtitle">Adicione, edite ou remova usuários do sistema.</p>
        </div>
        <button id="btn-novo-usuario" class="btn btn-primary">Novo Usuário</button>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Email</th>
              <th>Telefone</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody id="tabela-usuarios-body">
          </tbody>
        </table>
      </div>

      <div id="modal-usuario" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h2 id="modal-title">Novo Usuário</h2>
            <span class="close-modal" id="close-form-modal">&times;</span>
          </div>
          <form id="form-usuario">
            <input type="hidden" id="user-id">
            <div class="form-group">
              <label for="user-nome">Nome Completo</label>
              <input type="text" id="user-nome" required>
            </div>
            <div class="form-group">
              <label for="user-email">Email</label>
              <input type="email" id="user-email" required>
            </div>
            <div class="form-group">
              <label for="user-telefone">Telefone</label>
              <input type="text" id="user-telefone" required>
            </div>
            <div class="form-group">
              <label for="user-status">Status</label>
              <select id="user-status" required>
                <option value="Ativo">Ativo</option>
                <option value="Inativo">Inativo</option>
              </select>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" id="cancel-form-btn">Cancelar</button>
              <button type="submit" class="btn btn-primary">Salvar</button>
            </div>
          </form>
        </div>
      </div>

      <div id="modal-delete" class="modal">
        <div class="modal-content modal-delete-content">
          <div class="modal-header">
            <h2>Confirmar Exclusão</h2>
            <span class="close-modal" id="close-delete-modal">&times;</span>
          </div>
          <div class="modal-body">
            <p>Tem certeza que deseja excluir este usuário? Esta ação não pode ser desfeita.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" id="cancel-delete-btn">Cancelar</button>
            <button type="button" class="btn btn-danger" id="confirm-delete-btn">Excluir</button>
          </div>
        </div>
      </div>
    </div>
  `;
}

export function initUsuarios() {
  const tbody = document.getElementById('tabela-usuarios-body');
  
  const modalForm = document.getElementById('modal-usuario');
  const btnNovo = document.getElementById('btn-novo-usuario');
  const closeFormModalBtn = document.getElementById('close-form-modal');
  const cancelFormBtn = document.getElementById('cancel-form-btn');
  const form = document.getElementById('form-usuario');

  const inputId = document.getElementById('user-id');
  const inputNome = document.getElementById('user-nome');
  const inputEmail = document.getElementById('user-email');
  const inputTelefone = document.getElementById('user-telefone');
  const inputStatus = document.getElementById('user-status');
  const modalTitle = document.getElementById('modal-title');

  const modalDelete = document.getElementById('modal-delete');
  const closeDeleteModalBtn = document.getElementById('close-delete-modal');
  const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
  const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
  
  let userToDeleteId = null;

  function getUsuarios() {
    const data = localStorage.getItem('bibbleteca_usuarios');
    return data ? JSON.parse(data) : [];
  }

  function saveUsuarios(usuarios) {
    localStorage.setItem('bibbleteca_usuarios', JSON.stringify(usuarios));
  }

  function renderTable() {
    const usuarios = getUsuarios();
    tbody.innerHTML = '';
    
    if (usuarios.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Nenhum usuário cadastrado.</td></tr>';
      return;
    }

    usuarios.forEach(user => {
      const tr = document.createElement('tr');
      const statusClass = user.status === 'Ativo' ? 'badge-success' : 'badge-danger';
      
      tr.innerHTML = `
        <td>#${user.id}</td>
        <td><strong>${user.nome}</strong></td>
        <td>${user.email}</td>
        <td>${user.telefone}</td>
        <td><span class="badge ${statusClass}">${user.status}</span></td>
        <td class="actions-cell">
          <button class="btn-icon btn-edit" data-id="${user.id}">✎</button>
          <button class="btn-icon btn-delete" data-id="${user.id}">🗑</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    document.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', (e) => editUsuario(Number(e.target.dataset.id)));
    });

    document.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', (e) => openDeleteModal(Number(e.target.dataset.id)));
    });
  }

  function openFormModal(isEdit = false) {
    modalTitle.textContent = isEdit ? 'Editar Usuário' : 'Novo Usuário';
    modalForm.classList.add('show');
  }

  function closeFormModal() {
    modalForm.classList.remove('show');
    form.reset();
    inputId.value = '';
  }

  function openDeleteModal(id) {
    userToDeleteId = id;
    modalDelete.classList.add('show');
  }

  function closeDeleteModal() {
    modalDelete.classList.remove('show');
    userToDeleteId = null;
  }

  function editUsuario(id) {
    const usuarios = getUsuarios();
    const user = usuarios.find(u => u.id === id);
    if (user) {
      inputId.value = user.id;
      inputNome.value = user.nome;
      inputEmail.value = user.email;
      inputTelefone.value = user.telefone;
      inputStatus.value = user.status;
      openFormModal(true);
    }
  }

  function performDelete() {
    if (userToDeleteId !== null) {
      const usuarios = getUsuarios();
      const filtered = usuarios.filter(u => u.id !== userToDeleteId);
      saveUsuarios(filtered);
      renderTable();
      closeDeleteModal();
    }
  }

  btnNovo.addEventListener('click', () => openFormModal(false));
  closeFormModalBtn.addEventListener('click', closeFormModal);
  cancelFormBtn.addEventListener('click', closeFormModal);

  closeDeleteModalBtn.addEventListener('click', closeDeleteModal);
  cancelDeleteBtn.addEventListener('click', closeDeleteModal);
  confirmDeleteBtn.addEventListener('click', performDelete);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const usuarios = getUsuarios();
    const isEdit = inputId.value !== '';
    
    if (isEdit) {
      const index = usuarios.findIndex(u => u.id === Number(inputId.value));
      if (index !== -1) {
        usuarios[index] = {
          id: Number(inputId.value),
          nome: inputNome.value,
          email: inputEmail.value,
          telefone: inputTelefone.value,
          status: inputStatus.value
        };
      }
    } else {
      const newId = usuarios.length > 0 ? Math.max(...usuarios.map(u => u.id)) + 1 : 1;
      usuarios.push({
        id: newId,
        nome: inputNome.value,
        email: inputEmail.value,
        telefone: inputTelefone.value,
        status: inputStatus.value
      });
    }
    
    saveUsuarios(usuarios);
    closeFormModal();
    renderTable();
  });

  renderTable();
}