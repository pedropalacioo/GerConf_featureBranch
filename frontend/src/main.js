import './style.css';
import { renderNavbar } from './components/navbar.js';
import { renderDashboard } from './components/dashboard.js';

const app = document.querySelector('#app');

app.innerHTML = `
  ${renderNavbar()}
  <main id="content">
    ${renderDashboard()}
  </main>
`;
