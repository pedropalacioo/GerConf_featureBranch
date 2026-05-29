import './style.css';
import { renderNavbar } from './components/navbar.js';
import { renderDashboard } from './components/dashboard.js';
import { renderUsuarios, initUsuarios } from './components/usuarios.js';

const app = document.querySelector('#app');

app.innerHTML = `
  ${renderNavbar()}
  <main id="content"></main>
`;

const content = document.querySelector('#content');
const navItems = document.querySelectorAll('.nav-item');

function navigate(page) {
  navItems.forEach(item => {
    item.classList.remove('active');
    if (item.dataset.page === page) {
      item.classList.add('active');
    }
  });

  if (page === 'dashboard') {
    content.innerHTML = renderDashboard();
  } else if (page === 'usuarios') {
    content.innerHTML = renderUsuarios();
    initUsuarios();
  } else {
    content.innerHTML = `
      <div class="page-container">
        <div class="page-header">
          <h1 class="page-title">Em Construção</h1>
          <p class="page-subtitle">Esta página será implementada em breve.</p>
        </div>
      </div>
    `;
  }
}

navItems.forEach(item => {
  item.addEventListener('click', () => {
    const page = item.dataset.page;
    if (page) navigate(page);
  });
});

navigate('dashboard');
