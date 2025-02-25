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
            <h3>Repas servis aujourd'hui</h3>
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
      console.log('Checking admin access, user type:', this.authStore.userType);
      if (this.authStore.userType !== 'school_admin') {
        console.log('Unauthorized access, redirecting to login');
        this.$router.push('/admin/login');
      } else {
        console.log('Admin access granted, fetching dashboard data');
        this.fetchDashboardData();
      }
    },
    async fetchDashboardData() {
      try {
        const response = await api.get('admin/dashboard-stats/');
        this.stats = response.data;
        console.log('Dashboard data fetched:', this.stats);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Gérer l'erreur (par exemple, afficher un message à l'utilisateur)
      }
    },
    navigateTo(section) {
      console.log(`Navigating to ${section}`);
      // Implémenter la navigation vers les différentes sections
    },
    async performAction(action) {
      console.log(`Performing action: ${action}`);
      // Implémenter les actions spécifiques
    },
    async logout() {
      try {
        await this.authStore.logout();
        console.log('Logout successful, redirecting to login page');
        this.$router.push('/admin/login');
      } catch (error) {
        console.error('Error during logout:', error);
        // Gérer l'erreur de déconnexion
      }
    }
  }
};
</script>

<style scoped>
.admin-dashboard {
  background-color: #E3E3E3;
  min-height: 100vh;
  font-family: Arial, sans-serif;
}

.header {
  background-color: #436F8A; /* Bleu pétrole */
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

.btn-primary, .btn-logout, .btn-secondary {
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #FFB347; /* Orange doux */
  color: #FFFFFF;
}

.btn-primary:hover {
  background-color: #FFA500;
}

.btn-logout {
  background-color: #FF6F61; /* Rouge doux */
  color: #FFFFFF;
}

.btn-logout:hover {
  background-color: #FF5722;
}

.btn-secondary {
  background-color: #A8D5BA; /* Vert doux */
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
  background-color: #AEDFF7; /* Bleu ciel doux */
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
  color: #FF6F61; /* Rouge doux pour les alertes */
}

.action-buttons, .calendar-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

h2 {
  color: #436F8A; /* Bleu pétrole */
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
