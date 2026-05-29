export function renderReservas() {
  return `
    <div class="page-container">
      <div class="page-header">
        <div>
          <h1 class="page-title">Gerenciamento de Reservas</h1>
          <p class="page-subtitle">Controle as reservas de livros feitas pelos usuários.</p>
        </div>
        <button id="btn-nova-reserva" class="btn btn-primary">Nova Reserva</button>
      </div>

      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Leitor</th>
              <th>Livro</th>
              <th>Data</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody id="tabela-reservas-body">
          </tbody>
        </table>
      </div>

      <div id="modal-reserva" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h2 id="modal-title">Nova Reserva</h2>
            <span class="close-modal" id="close-form-modal">&times;</span>
          </div>
          <form id="form-reserva">
            <input type="hidden" id="reserva-id">
            <div class="form-group">
              <label for="reserva-leitor">Nome do Leitor</label>
              <input type="text" id="reserva-leitor" required>
            </div>
            <div class="form-group">
              <label for="reserva-livro">Título do Livro</label>
              <input type="text" id="reserva-livro" required>
            </div>
            <div class="form-group">
              <label for="reserva-data">Data da Reserva</label>
              <input type="date" id="reserva-data" required>
            </div>
            <div class="form-group">
              <label for="reserva-status">Status</label>
              <select id="reserva-status" required>
                <option value="Pendente">Pendente</option>
                <option value="Confirmada">Confirmada</option>
                <option value="Cancelada">Cancelada</option>
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
            <p>Tem certeza que deseja excluir esta reserva? Esta ação não pode ser desfeita.</p>
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

export function initReservas() {
  const tbody = document.getElementById('tabela-reservas-body');
  
  const modalForm = document.getElementById('modal-reserva');
  const btnNova = document.getElementById('btn-nova-reserva');
  const closeFormModalBtn = document.getElementById('close-form-modal');
  const cancelFormBtn = document.getElementById('cancel-form-btn');
  const form = document.getElementById('form-reserva');

  const inputId = document.getElementById('reserva-id');
  const inputLeitor = document.getElementById('reserva-leitor');
  const inputLivro = document.getElementById('reserva-livro');
  const inputData = document.getElementById('reserva-data');
  const inputStatus = document.getElementById('reserva-status');
  const modalTitle = document.getElementById('modal-title');

  const modalDelete = document.getElementById('modal-delete');
  const closeDeleteModalBtn = document.getElementById('close-delete-modal');
  const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
  const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
  
  let reservaToDeleteId = null;

  function getReservas() {
    const data = localStorage.getItem('bibbleteca_reservas');
    return data ? JSON.parse(data) : [];
  }

  function saveReservas(reservas) {
    localStorage.setItem('bibbleteca_reservas', JSON.stringify(reservas));
  }

  function formatDateBR(dateString) {
    if (!dateString) return '';
    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year}`;
  }

  function renderTable() {
    const reservas = getReservas();
    tbody.innerHTML = '';
    
    if (reservas.length === 0) {
      tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Nenhuma reserva cadastrada.</td></tr>';
      return;
    }

    reservas.forEach(reserva => {
      const tr = document.createElement('tr');
      
      let statusClass = 'badge-warning';
      if (reserva.status === 'Confirmada') statusClass = 'badge-success';
      if (reserva.status === 'Cancelada') statusClass = 'badge-danger';
      
      tr.innerHTML = `
        <td>#${reserva.id}</td>
        <td><strong>${reserva.leitor}</strong></td>
        <td>${reserva.livro}</td>
        <td>${formatDateBR(reserva.data)}</td>
        <td><span class="badge ${statusClass}">${reserva.status}</span></td>
        <td class="actions-cell">
          <button class="btn-icon btn-edit" data-id="${reserva.id}">✎</button>
          <button class="btn-icon btn-delete" data-id="${reserva.id}">🗑</button>
        </td>
      `;
      tbody.appendChild(tr);
    });

    document.querySelectorAll('.btn-edit').forEach(btn => {
      btn.addEventListener('click', (e) => editReserva(Number(e.target.dataset.id)));
    });

    document.querySelectorAll('.btn-delete').forEach(btn => {
      btn.addEventListener('click', (e) => openDeleteModal(Number(e.target.dataset.id)));
    });
  }

  function openFormModal(isEdit = false) {
    modalTitle.textContent = isEdit ? 'Editar Reserva' : 'Nova Reserva';
    modalForm.classList.add('show');
  }

  function closeFormModal() {
    modalForm.classList.remove('show');
    form.reset();
    inputId.value = '';
  }

  function openDeleteModal(id) {
    reservaToDeleteId = id;
    modalDelete.classList.add('show');
  }

  function closeDeleteModal() {
    modalDelete.classList.remove('show');
    reservaToDeleteId = null;
  }

  function editReserva(id) {
    const reservas = getReservas();
    const reserva = reservas.find(r => r.id === id);
    if (reserva) {
      inputId.value = reserva.id;
      inputLeitor.value = reserva.leitor;
      inputLivro.value = reserva.livro;
      inputData.value = reserva.data;
      inputStatus.value = reserva.status;
      openFormModal(true);
    }
  }

  function performDelete() {
    if (reservaToDeleteId !== null) {
      const reservas = getReservas();
      const filtered = reservas.filter(r => r.id !== reservaToDeleteId);
      saveReservas(filtered);
      renderTable();
      closeDeleteModal();
    }
  }

  btnNova.addEventListener('click', () => {
    form.reset();
    inputData.value = new Date().toISOString().split('T')[0];
    openFormModal(false);
  });
  
  closeFormModalBtn.addEventListener('click', closeFormModal);
  cancelFormBtn.addEventListener('click', closeFormModal);

  closeDeleteModalBtn.addEventListener('click', closeDeleteModal);
  cancelDeleteBtn.addEventListener('click', closeDeleteModal);
  confirmDeleteBtn.addEventListener('click', performDelete);

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const reservas = getReservas();
    const isEdit = inputId.value !== '';
    
    if (isEdit) {
      const index = reservas.findIndex(r => r.id === Number(inputId.value));
      if (index !== -1) {
        reservas[index] = {
          id: Number(inputId.value),
          leitor: inputLeitor.value,
          livro: inputLivro.value,
          data: inputData.value,
          status: inputStatus.value
        };
      }
    } else {
      const newId = reservas.length > 0 ? Math.max(...reservas.map(r => r.id)) + 1 : 1;
      reservas.push({
        id: newId,
        leitor: inputLeitor.value,
        livro: inputLivro.value,
        data: inputData.value,
        status: inputStatus.value
      });
    }
    
    saveReservas(reservas);
    closeFormModal();
    renderTable();
  });

  renderTable();
}
