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
            <h3>total repas / jour</h3>
            <p class="stat-number">{{ animatedMeals }}</p>
          </div>
          <div class="stat-card">
            <h3>Élèves inscrits</h3>
            <p class="stat-number">{{ animatedStudents }}</p>
          </div>
          <div class="stat-card">
            <h3>Allergies signalées</h3>
            <p class="stat-number" :class="{ warning: stats.reportedAllergies > 20 }">
              {{ animatedAllergies }}
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
          <button class="btn-secondary" @click="showAddParentModal">Ajouter un parent</button>
          <button class="btn-secondary" @click="performAction('correctData')">Corriger les données</button>
        </div>
      </section>
      <AddParentModal :isVisible="isAddParentModalVisible" :closeModal="closeAddParentModal"
        @onParentAdded="fetchDashboardData" />

      <section class="calendar-section">
        <h2>Gestion du calendrier</h2>
        <div class="calendar-actions">
          <button class="btn-secondary" @click="performAction('setHolidays')">Définir les vacances</button>
          <button class="btn-secondary" @click="performAction('setClosures')">Fermetures
            exceptionnelles</button>
        </div>
      </section>

      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import api from '@/http-common';
import { defineAsyncComponent } from 'vue';

const AddParentModal = defineAsyncComponent(() => import('@/components/admin/AddParentModal.vue'));

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
      },
      isAddParentModalVisible: false,
    };
  },
  created() {
    this.checkAdminAccess();
  },
  methods: {
    checkAdminAccess() {
      if (this.authStore.userType !== 'school_admin') {
        this.$router.push('/');
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
      }
    },
    navigateTo(section) {
      switch (section) {
        case 'meals':
          this.$router.push('/admin/meals').catch(this.handleNavigationError);
          break;
        case 'students':
          this.$router.push('/admin/students').catch(this.handleNavigationError);
          break;
        case 'reports':
          this.$router.push('/admin/reports').catch(this.handleNavigationError);
          break;
        default:
          console.error(`Section inconnue : ${section}`);
      }
    },
    performAction(action) {
      console.log(`Action effectuée : ${action}`);
      switch (action) {
        case 'addMeal':
          this.$router.push('/admin/add-meal').catch(this.handleNavigationError);
          break;
        case 'enrollStudent':
          this.$router.push('/admin/enroll-student').catch(this.handleNavigationError);
          break;
        case 'generateReport':
          this.$router.push('/admin/generate-report').catch(this.handleNavigationError);
          break;
        case 'addAdmin':
          this.$router.push({ name: 'AddAdmin' }).catch(this.handleNavigationError);
          break;
        case 'correctData':
          this.$router.push('/admin/correct-data').catch(this.handleNavigationError);
          break;
        case 'setHolidays':
          this.$router.push('/admin/set-holidays').catch(this.handleNavigationError);
          break;
        case 'setClosures':
          this.$router.push('/admin/set-closures').catch(this.handleNavigationError);
          break;
        default:
          console.error(`Action inconnue : ${action}`);
      }
    },
    handleNavigationError(err) {
      if (err.name !== 'NavigationDuplicated') {
        console.error('Erreur de navigation:', err);
      }
    },
    showAddParentModal() {
      this.isAddParentModalVisible = true;
    },
    closeAddParentModal() {
      this.isAddParentModalVisible = false;
    },
    async logout() {
      try {
        await this.authStore.logout();
        this.$router.push('/');
      } catch (error) {
        console.error('Error during logout:', error);
      }
    },
    animateCounter(targetValue, duration = 2000) {
      const currentValue = ref(0);
      const startTime = Date.now();

      const updateCounter = () => {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);

        const easeOutQuad = progress * (2 - progress);
        currentValue.value = Math.round(targetValue * easeOutQuad);

        if (progress < 1) {
          requestAnimationFrame(updateCounter);
        } else {
          currentValue.value = targetValue;
        }

        return currentValue.value;
      };

      updateCounter();
      return currentValue;
    }
  },
  components: {
    AddParentModal
  },
  computed: {
    animatedMeals() {
      return this.animateCounter(this.stats.mealsServedToday).value;
    },
    animatedStudents() {
      return this.animateCounter(this.stats.enrolledStudents).value;
    },
    animatedAllergies() {
      return this.animateCounter(this.stats.reportedAllergies).value;
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

.btn-primary,
.btn-logout,
.btn-secondary {
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

.stats-section,
.actions-section,
.calendar-section {
  background-color: #ebe1d0;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  justify-content: center;
}

.stat-card {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  border: 2px solid #2e5626;
  background-color: transparent;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  transition: background-color 0.3s ease;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
  position: relative;
}

.stat-card:hover {
  background-color: #e8f5e9;
  cursor: pointer;
}

.stat-card h3 {
  color: #2e5626;
  font-size: 0.9rem;
  margin-top: 15px;
  position: relative;
  top: 0;
  bottom: auto;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #3A6351;
  text-align: center;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.warning {
  color: #FF6F61;
}

.action-buttons,
.calendar-actions {
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
