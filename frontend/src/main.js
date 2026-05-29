import './style.css';
import { renderNavbar } from './components/navbar.js';
import { renderDashboard } from './components/dashboard.js';
import { renderGerirLivros, initGerirLivros } from './components/gerirLivros.js';
import { renderEmprestimos, initEmprestimos } from './components/emprestimos.js';

const app = document.querySelector('#app');

// 1. Renderiza a estrutura inicial com o Dashboard por defeito
app.innerHTML = `
  ${renderNavbar()}
  <main id="content">
    ${renderDashboard()}
  </main>
`;

// 2. Lógica de navegação do menu lateral
const content = document.querySelector('#content');
const navItems = document.querySelectorAll('.nav-item');

navItems.forEach((item, index) => {
  item.addEventListener('click', () => {
    // Remove a classe 'active' de todos os itens do menu
    navItems.forEach(nav => nav.classList.remove('active'));
    
    // Adiciona a classe 'active' apenas ao item em que clicaste
    item.classList.add('active');

    // Troca o conteúdo principal dependendo do índice (posição do item no menu)
    if (index === 0) {
      // 1º Item: Dashboard
      content.innerHTML = renderDashboard();
    } else if (index === 1) {
      // 2º Item: Gerir Livros
      content.innerHTML = renderGerirLivros();
      initGerirLivros();
    } else if (index === 2) {
      // 3º Item: Empréstimos
      content.innerHTML = renderEmprestimos();
      initEmprestimos();
    } else {
      // Outros itens ainda não implementados
      content.innerHTML = `<div style="padding: 40px; text-align: center;">
                             <h2 class="bibble-text">Página em construção... ✨</h2>
                           </div>`;
    }
  });
});