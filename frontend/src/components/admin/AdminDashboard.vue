<template>
  <div class="admin-dashboard">
    <header class="header">
      <h1>Tableau de bord administrateur</h1>
      <nav>
        <button class="btn-primary">Gérer les repas</button>
        <button class="btn-primary">Gérer les élèves</button>
        <button class="btn-primary">Rapports</button>
        <button @click="logout" class="btn-logout">Déconnexion</button>
      </nav>
    </header>

    <main class="dashboard-content">
      <section class="stats-section">
        <h2>Statistiques</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <h3>Repas servis aujourd'hui</h3>
            <p class="stat-number">150</p>
          </div>
          <div class="stat-card">
            <h3>Élèves inscrits</h3>
            <p class="stat-number">500</p>
          </div>
          <div class="stat-card">
            <h3>Allergies signalées</h3>
            <p class="stat-number warning">25</p>
          </div>
        </div>
      </section>

      <section class="actions-section">
        <h2>Actions rapides</h2>
        <div class="action-buttons">
          <button class="btn-secondary">Ajouter un repas</button>
          <button class="btn-secondary">Inscrire un élève</button>
          <button class="btn-secondary">Générer un rapport</button>
          <button class="btn-secondary">Nouvel administrateur</button>
          <button class="btn-secondary">Ajouter un parent</button>
          <button class="btn-secondary">Corriger les données</button>
        </div>
      </section>

      <section class="calendar-section">
        <h2>Gestion du calendrier</h2>
        <div class="calendar-actions">
          <button class="btn-secondary">Définir les vacances</button>
          <button class="btn-secondary">Fermetures exceptionnelles</button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  methods: {
    logout() {
      // Supprimer le token d'authentification du stockage local
      localStorage.removeItem('authToken');
      
      // Rediriger vers la page d'accueil
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  background-color: #E3E3E3;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.header {
  background-color: #436F8A;
  color: #FFFFFF;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header h1 {
  margin: 0;
  font-size: 1.5rem;
}

nav {
  display: flex;
  gap: 1rem;
}

.btn-primary, .btn-logout {
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #FFB347;
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: #FFA500;
}

.btn-logout {
  background-color: #FF6F61;
  color: #FFFFFF;
}

.btn-logout:hover {
  background-color: #FF5722;
}

.dashboard-content {
  padding: 2rem;
  display: grid;
  gap: 2rem;
}

.stats-section, .actions-section, .calendar-section {
  background-color: #FFFFFF;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background-color: #AEDFF7;
  padding: 1rem;
  border-radius: 6px;
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #3A6351;
}

.warning {
  color: #FF6F61;
}

.action-buttons, .calendar-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.btn-secondary {
  background-color: #A8D5BA;
  color: #3A6351;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-secondary:hover {
  background-color: #8BC4A5;
}

h2 {
  color: #436F8A;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
  }

  nav {
    margin-top: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style>
