import './style.css';
import { renderNavbar } from './components/navbar.js';
import { renderDashboard } from './components/dashboard.js';
import { renderGerirLivros, initGerirLivros } from './components/gerirLivros.js'; // Importação atualizada

const app = document.querySelector('#app');

app.innerHTML = `
  ${renderNavbar()}
  <main id="content">
    ${renderDashboard()}
  </main>
`;

const content = document.querySelector('#content');
const navItems = document.querySelectorAll('.nav-item');

navItems.forEach((item, index) => {
  item.addEventListener('click', () => {
    navItems.forEach(nav => nav.classList.remove('active'));
    item.classList.add('active');

    if (index === 0) {
      content.innerHTML = renderDashboard();
    } else if (index === 1) {
      content.innerHTML = renderGerirLivros();
      initGerirLivros(); // MÁGICA: Inicia os eventos (cliques, form) da página de livros!
    } else {
      content.innerHTML = `<div style="padding: 40px; text-align: center;">
                             <h2 class="bibble-text">Página em construção... ✨</h2>
                           </div>`;
    }
  });
});