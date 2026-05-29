export function renderDashboard() {
  return /*html*/`
    <div class="dashboard-container">
      <div class="dashboard-header">
        <h1 class="dashboard-title">Dashboard Principal</h1>
        <p class="dashboard-subtitle">Bem-vindo ao Sistema de Gestão da Biblioteca.</p>
      </div>
      
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon icon-blue">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
          </div>
          <div class="stat-details">
            <h3>Total de Livros</h3>
            <p class="stat-value text-blue">124</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon icon-green">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <div class="stat-details">
            <h3>Disponíveis</h3>
            <p class="stat-value text-green">89</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon icon-orange">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="stat-details">
            <h3>Empréstimos Ativos</h3>
            <p class="stat-value text-orange">35</p>
          </div>
        </div>

        <div class="stat-card">
          <div class="stat-icon icon-purple">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </div>
          <div class="stat-details">
            <h3>Usuários</h3>
            <p class="stat-value text-purple">42</p>
          </div>
        </div>
      </div>
    </div>
  `;
}
