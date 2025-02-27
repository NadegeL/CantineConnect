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
                console.error('Erreur lors de la récupération des statistiques du tableau de bord:', error);
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
                this.$router.push('/admin/login');
            } catch (error) {
        console.error('Error during logout:', error);
        // Handling disconnection errors
            }
        }
    },
    components: {
        AddParentModal
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
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
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

.action-buttons,
.calendar-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
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
