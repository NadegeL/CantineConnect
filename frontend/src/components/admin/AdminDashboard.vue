<template>
  <div class="admin-dashboard">
    <header class="header">
      <h1>Tableau de bord administrateur</h1>
      <nav>
        <button class="btn-primary" @click="navigateTo('meals')">Gérer les repas</button>
        <button class="btn-primary" @click="navigateTo('students')">Gérer les élèves</button>
        <button class="btn-primary" @click="navigateTo('reports')">Rapports</button>
        <button @click="logout" class="btn-logout">Déconnexion</button>
      </nav>
    </header>

    <main class="dashboard-content">
      <section class="stats-section">
        <h2>Statistiques</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <h3> total repas / jour</h3>
            <p class="stat-number">{{ stats.mealsServedToday }}</p>
          </div>
          <div class="stat-card">
            <h3>Élèves inscrits</h3>
            <p class="stat-number">{{ stats.enrolledStudents }}</p>
          </div>
          <div class="stat-card">
            <h3>Allergies signalées</h3>
            <p class="stat-number" :class="{ warning: stats.reportedAllergies > 20 }">
              {{ stats.reportedAllergies }}
            </p>
          </div>
        </div>
      </section>

      <section class="actions-section">
        <h2>Actions rapides</h2>
        <div class="action-buttons">
          <button class="btn-secondary" @click="performAction('addMeal')">Ajouter un repas</button>
          <button class="btn-secondary" @click="performAction('enrollStudent')">Inscrire un élève</button>
          <button class="btn-secondary" @click="performAction('generateReport')">Générer un rapport</button>
          <button class="btn-secondary" @click="performAction('addAdmin')">Nouvel administrateur</button>
          <button class="btn-secondary" @click="performAction('addParent')">Ajouter un parent</button>
          <button class="btn-secondary" @click="performAction('correctData')">Corriger les données</button>
        </div>
      </section>

      <section class="calendar-section">
        <h2>Gestion du calendrier</h2>
        <div class="calendar-actions">
          <button class="btn-secondary" @click="performAction('setHolidays')">Définir les vacances</button>
          <button class="btn-secondary" @click="performAction('setClosures')">Fermetures exceptionnelles</button>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import api from '@/http-common';

export default {
  name: 'AdminDashboard',
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      stats: {
        mealsServedToday: 0,
        enrolledStudents: 0,
        reportedAllergies: 0
      }
    };
  },
  created() {
    this.checkAdminAccess();
  },
  methods: {
    checkAdminAccess() {
      if (this.authStore.userType !== 'school_admin') {
        this.$router.push('/admin/login');
      } else {
        this.fetchDashboardData();
      }
    },
    async fetchDashboardData() {
      try {
        const response = await api.get('admin/dashboard-stats/');
        this.stats = response.data;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Handle the error (e.g. display a message to the user)
      }
    },
    navigateTo(section) {
      // Implement navigation to the various sections
    },
    async performAction(action) {
      // Implement specific actions
    },
    async logout() {
      try {
        await this.authStore.logout();
        this.$router.push('/admin/login');
      } catch (error) {
        console.error('Error during logout:', error);
        // Handling disconnection errors
      }
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  background-color: #e8f5e8;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.header {
  background-color: #2e5626;
  color: #ebe1d0;
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

.btn-primary, .btn-logout, .btn-secondary {
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #2e5626;
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: #4a7b2a;
}

.btn-logout {
  background-color: #951509;
  color: #FFFFFF;
}

.btn-logout:hover {
  background-color: #FF5722;
}

.btn-secondary {
  background-color: #A8D5BA;
  color: #3A6351;
}

.btn-secondary:hover {
  background-color: #8BC4A5;
}

.dashboard-content {
  padding: 2rem;
  display: grid;
  gap: 2rem;
}

.stats-section, .actions-section, .calendar-section {
  background-color: #ebe1d0;
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
  width: 200px;  /* Taille fixe */
  height: 200px; /* Carré/Cercle parfait */
  border-radius: 50%; /* Crée un cercle parfait */
  border: 2px solid #2e5626; /* Liseré vert foncé */
  background-color: transparent; /* Fond transparent */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: background-color 0.3s ease;
  margin: 0 auto; /* Centre les cartes dans leur cellule de grille */
  padding: 20px;
  text-align: center;
}

.stat-card:hover {
  background-color: #e8f5e9; /* Vert clair s'illumine au survol */
  cursor: pointer;
}

.stat-card h3 {
  color: #2e5626;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 15px;
  flex-grow: 0;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #3A6351;
  text-align: center;
  margin-top: 10px;
}

.warning {
  color: #FF6F61;
}

.action-buttons, .calendar-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

h2 {
  color: #2e5626;
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