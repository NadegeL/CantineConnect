<template>
  <div class="parent-dashboard">
    <h1>Tableau de bord Parent</h1>
    <button @click="logoutUser" class="btn-logout">Déconnexion</button>
    <button @click="goToUpdateProfile" class="btn-update-profile">Mettre à jour le profil</button>

    <WelcomeModal v-if="showWelcomeModal" @close="openProfileModal" />
    <ProfileModal v-if="showProfileModal" :parentData="parentData" @save="saveProfile" @close="closeProfileModal" />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import WelcomeModal from './WelcomeModal.vue';
import ProfileModal from './ProfileModal.vue';
import { fetchParentProfile, saveProfile } from '@/services/parentService';
import { logout } from '@/services/authService';

export default {
  name: 'ParentsDashboard',
  components: { WelcomeModal, ProfileModal },
  setup() {
    const router = useRouter();
    const showWelcomeModal = ref(false);
    const showProfileModal = ref(false);
    const parentData = ref(null);
    const authStore = useAuthStore();

    const isProfileComplete = () => {
      return (
        parentData.value &&
        parentData.value.user.first_name &&
        parentData.value.user.last_name &&
        parentData.value.address &&
        parentData.value.phone_number
      );
    };

    const checkFirstLogin = async () => {
      console.log('Vérification de la première connexion...');
      if (!isProfileComplete()) {
        console.log('Profil incomplet, affichage de la modale de bienvenue.');
        showWelcomeModal.value = true;
      } else {
        console.log('Profil complet, pas besoin d\'afficher la modale.');
      }
    };

    const getParentProfile = async () => {
      try {
        console.log('Récupération du profil parent...');
        const data = await fetchParentProfile();
        parentData.value = data;
        console.log('Profil parent récupéré :', parentData.value);
      } catch (error) {
        console.error('Erreur lors de la récupération du profil :', error);
      }
    };

    const updateProfile = async (profileData) => {
      try {
        console.log('Envoi des données pour mise à jour du profil :', profileData);
        await saveProfile(profileData);
        await getParentProfile();
        showProfileModal.value = false;
      } catch (error) {
        console.error('Erreur lors de la mise à jour du profil :', error);
      }
    };

    const openProfileModal = () => {
      console.log('Ouverture de la modale pour compléter les informations.');
      showWelcomeModal.value = false;
      showProfileModal.value = true;
    };

    const closeProfileModal = () => {
      console.log('Fermeture de la modale.');
      showProfileModal.value = false;
    };

    const goToUpdateProfile = () => {
      console.log('Redirection vers la page de mise à jour du profil.');
      router.push('/parent/update-profile');
    };

    const logoutUser = async () => {
      try {
        console.log('Déconnexion...');
        await logout();
        router.push('/');
      } catch (error) {
        console.error('Erreur lors de la déconnexion:', error);
      }
    };

    onMounted(async () => {
      console.log('Montage du composant ParentsDashboard.');
      await getParentProfile();
      checkFirstLogin();
    });

    return {
      showWelcomeModal,
      showProfileModal,
      parentData,
      updateProfile,
      openProfileModal,
      closeProfileModal,
      goToUpdateProfile,
      logoutUser,
    };
  },
};
</script>

<style scoped>
.parent-dashboard {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.btn-logout,
.btn-update-profile {
  margin: 10px;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-logout {
  background-color: #f44336;
  color: white;
}

.btn-update-profile {
  background-color: #4CAF50;
  color: white;
}
</style>
