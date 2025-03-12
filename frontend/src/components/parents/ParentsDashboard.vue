<template>
  <div class="dashboard-page" :style="{ backgroundImage: `url(${logoPath})` }">
    <div class="overlay" :class="{ 'fade-in': backgroundLoaded }"></div>

    <!-- Boutons Déconnexion et Profil -->
    <div class="flex justify-between items-center px-4 py-3">
      <button @click="logoutUser"
        class="bg-red-600 hover:bg-red-700 text-white py-2 px-4 rounded-md flex items-center gap-2 transition-colors">
        <span class="i-mdi:logout w-5 h-5"></span>
        Déconnexion
      </button>
      <button @click="goToUpdateProfile"
        class="bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md flex items-center gap-2 transition-colors">
        <span class="i-mdi:account-edit w-5 h-5"></span>
        Mettre à jour le profil
      </button>
    </div>

    <div class="content-container">
      <!-- Titre centré et en vert foncé -->
      <h1 class="text-center text-green-800 text-3xl font-bold py-8">Mon Dossier</h1>

      <div class="flex justify-between max-w-4xl mx-auto px-4">
        <!-- Liste des sections à gauche -->
        <div class="w-full md:w-2/3">
          <!-- Section Enfants -->
          <div class="mb-4">
            <div class="flex items-center bg-white bg-opacity-80 p-4 rounded-lg cursor-pointer shadow-sm"
              @click="toggleSection('enfants')">
              <div class="bg-green-100 p-3 rounded-md mr-4">
                <span class="i-mdi:account-group text-2xl text-green-800"></span>
              </div>
              <h2 class="text-xl font-semibold text-green-800">Enfants({{ enfants.length }})</h2>
              <div class="flex gap-2 ml-4">
                <button @click.stop="openCreateStudentModal"
                  class="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm transition-colors flex items-center gap-1">
                  <span class="i-mdi:plus w-4 h-4"></span>
                  Ajouter
                </button>
              </div>
              <div class="ml-auto">
                <div class="i-mdi-chevron-right text-xl text-green-800" :class="{ 'rotate-90': sections.enfants }">
                </div>
              </div>
            </div>
            <!-- Contenu de la section Enfants -->
            <div v-show="sections.enfants"
              class="mt-2 pl-16 pr-4 py-2 transition-all duration-300 bg-white bg-opacity-90 rounded-lg">
              <div v-if="enfants.length === 0" class="text-gray-500">
                Aucun enfant enregistré
              </div>
              <div v-for="enfant in enfants" :key="enfant.id" class="border-b border-green-100 py-3">
                <h3 class="font-medium">{{ enfant.prenom }} {{ enfant.nom }}</h3>
                <!-- Utilisation de la méthode pour obtenir le nom de la classe -->
                <p class="text-gray-600">Classe: {{ getClassName(enfant.classe) }}</p>
                <p class="text-gray-600">
                  Statut cantine:
                  <span :class="enfant.inscrit_cantine ? 'text-green-600' : 'text-red-600'">
                    {{ enfant.inscrit_cantine ? 'Inscrit' : 'Non inscrit' }}
                  </span>
                </p>
              </div>
            </div>
          </div>

          <!-- Section Responsables légaux -->
          <div class="mb-4">
            <div class="flex items-center bg-white bg-opacity-80 p-4 rounded-lg cursor-pointer shadow-sm"
              @click="toggleSection('responsables')">
              <div class="bg-green-100 p-3 rounded-md mr-4">
                <span class="i-mdi:account text-2xl text-green-800"></span>
              </div>
              <h2 class="text-xl font-semibold text-green-800">Responsables légaux({{ responsables.length }})</h2>
              <div class="flex gap-2 ml-4">
                <button @click.stop="modifyItem('responsables')"
                  class="bg-amber-500 hover:bg-amber-600 text-white py-1 px-3 rounded-md text-sm transition-colors flex items-center gap-1">
                  <span class="i-mdi-pencil w-4 h-4"></span>
                  Modifier
                </button>
              </div>
              <div class="ml-auto">
                <div class="i-mdi-chevron-right text-xl text-green-800" :class="{ 'rotate-90': sections.responsables }">
                </div>
              </div>
            </div>
            <!-- Contenu de la section Responsables -->
            <div v-show="sections.responsables"
              class="mt-2 pl-16 pr-4 py-2 transition-all duration-300 bg-white bg-opacity-90 rounded-lg">
              <div v-for="responsable in responsables" :key="responsable.id" class="border-b border-green-100 py-3">
                <h3 class="font-medium">{{ responsable.prenom }} {{ responsable.nom }}</h3>
                <p class="text-gray-600">Téléphone: {{ responsable.telephone }}</p>
                <p class="text-gray-600">Email: {{ responsable.email }}</p>
                <p class="text-gray-600">Adresse: {{ responsable.adresse }}</p>
              </div>
            </div>
          </div>

          <!-- Section Justificatifs d'absence -->
          <div class="mb-4">
            <div class="flex items-center bg-white bg-opacity-80 p-4 rounded-lg cursor-pointer shadow-sm"
              @click="toggleSection('justificatifs')">
              <div class="bg-green-100 p-3 rounded-md mr-4">
                <span class="i-mdi-file-document text-2xl text-green-800"></span>
              </div>
              <h2 class="text-xl font-semibold text-green-800">Justificatifs d'absence</h2>
              <div class="flex gap-2 ml-4">
                <button @click.stop="addItem('justificatifs')"
                  class="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm transition-colors flex items-center gap-1">
                  <span class="i-mdi:plus w-4 h-4"></span>
                  Ajouter
                </button>
              </div>
              <div class="ml-auto">
                <div class="i-mdi-chevron-right text-xl text-green-800"
                  :class="{ 'rotate-90': sections.justificatifs }">
                </div>
              </div>
            </div>
            <!-- Contenu de la section Justificatifs -->
            <div v-show="sections.justificatifs"
              class="mt-2 pl-16 pr-4 py-2 transition-all duration-300 bg-white bg-opacity-90 rounded-lg">
              <div v-if="justificatifs.length === 0" class="text-gray-500">
                Aucun justificatif d'absence
              </div>
              <div v-for="justif in justificatifs" :key="justif.id" class="border-b border-green-100 py-3">
                <h3 class="font-medium">{{ justif.date }}</h3>
                <p class="text-gray-600">Enfant: {{ justif.enfant }}</p>
                <p class="text-gray-600">Motif: {{ justif.motif }}</p>
              </div>
            </div>
          </div>

          <!-- Section Allergies/PAI -->
          <div class="mb-4">
            <div class="flex items-center bg-white bg-opacity-80 p-4 rounded-lg cursor-pointer shadow-sm"
              @click="toggleSection('allergies')">
              <div class="bg-green-100 p-3 rounded-md mr-4">
                <span class="i-mdi-alert text-2xl text-green-800"></span>
              </div>
              <h2 class="text-xl font-semibold text-green-800">Allergies/PAI</h2>
              <div class="flex gap-2 ml-4">
                <button @click.stop="openAddAllergyModal"
                  class="bg-green-600 hover:bg-green-700 text-white py-1 px-3 rounded-md text-sm transition-colors flex items-center gap-1">
                  <span class="i-mdi:plus w-4 h-4"></span>
                  Ajouter
                </button>
              </div>
              <div class="ml-auto">
                <div class="i-mdi-chevron-right text-xl text-green-800" :class="{ 'rotate-90': sections.allergies }">
                </div>
              </div>
            </div>
            <!-- Contenu de la section Allergies -->
            <div v-show="sections.allergies"
              class="mt-2 pl-16 pr-4 py-2 transition-all duration-300 bg-white bg-opacity-90 rounded-lg">
              <div v-if="allergies.length === 0" class="text-gray-500">
                Aucune allergie ou PAI enregistré
              </div>
              <div v-for="allergie in allergies" :key="allergie.id" class="border-b border-green-100 py-3">
                <h3 class="font-medium">{{ allergie.enfant }}</h3>
                <p class="text-gray-600">Type: {{ allergie.type }}</p>
                <!-- Affichage de la sévérité avec couleur et traduction -->
                <p class="text-gray-600">
                  Sévérité:
                  <span :class="severityColor(allergie.severity)">
                    {{ translateSeverity(allergie.severity) }}
                  </span>
                </p>
                <p class="text-gray-600">Description: {{ allergie.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Bulle d'information du parent à droite -->
        <div class="hidden md:block md:w-1/3">
          <div class="bg-white bg-opacity-90 rounded-3xl shadow-md p-8 ml-4">
            <div class="flex flex-col items-center">
              <div class="bg-green-100 w-20 h-20 flex items-center justify-center rounded-full mb-4">
                <span class="text-2xl font-bold text-green-800">{{ getInitials(parent.prenom, parent.nom) }}</span>
              </div>
              <h2 class="text-2xl font-bold text-green-800">{{ parent.prenom }} {{ parent.nom }}</h2>
              <div class="mt-4 w-full space-y-2">
                <p class="text-gray-600">Parents</p>
                <p class="text-gray-600">Contact d'urgence</p>
                <p class="text-gray-600">Payeur</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showWelcomeModal" class="modal-overlay">
      <div class="modal-content">
        <WelcomeModal @close="openProfileModal" />
      </div>
    </div>


    <div v-if="showProfileModal" class="modal-overlay">
      <div class="modal-content">
        <ProfileModal :parentData="parentData" @save="saveProfile" @close="closeProfileModal" />
      </div>
    </div>

    <!-- Modale de création d'élève -->
    <CreateStudentModal v-if="showCreateStudentModal" :showModal="showCreateStudentModal" :parentId="parentId"
      @close="closeCreateStudentModal" @create="handleCreateStudent" />

    <!-- Ajout de la modale AddAllergyModal -->
    <AddAllergyModal v-if="showAddAllergyModal" :students="students" @close="closeAddAllergyModal"
      @created="handleAllergyCreated" />
  </div>
</template>

<script>
import { ref, onMounted, onBeforeMount } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import WelcomeModal from './WelcomeModal.vue';
import ProfileModal from './ProfileModal.vue';
import CreateStudentModal from './CreateStudentModal.vue';
import AddAllergyModal from './AddAllergyModal.vue';
import { fetchParentProfile, saveProfile } from '@/services/parentService';
import { fetchStudentsByParent, fetchStudentAllergies, fetchClasses } from '@/services/studentService';
import { logout } from '@/services/authService';
import logoImage from '@/assets/Logo.png';

export default {
  name: 'ParentDashboard',
  components: { WelcomeModal, ProfileModal, CreateStudentModal, AddAllergyModal },
  data() {
    return {
      logoPath: logoImage,
      backgroundLoaded: false,
      parent: {
        nom: 'Luthier',
        prenom: 'Nadège',
        email: 'nadege.luthier@example.com',
        telephone: '06 12 34 56 78',
        adresse: '123 Rue de l\'École, 75001 Paris'
      },
      enfants: [],
      responsables: [],
      justificatifs: [],
      allergies: [],
      sections: {
        enfants: false,
        responsables: false,
        justificatifs: false,
        allergies: false
      },
      classes: []
    }
  },
  setup() {
    const router = useRouter();
    const showWelcomeModal = ref(false);
    const showProfileModal = ref(false);
    const showCreateStudentModal = ref(false);
    const showAddAllergyModal = ref(false);
    const parentData = ref(null);
    const parentId = ref(null);
    const authStore = useAuthStore();
    const logoPath = ref(logoImage);
    const backgroundLoaded = ref(false);
    const enfants = ref([]);
    const responsables = ref([]);
    const justificatifs = ref([]);
    const allergies = ref([]);
    const students = ref([]);
    const sections = ref({
      enfants: false,
      responsables: false,
      justificatifs: false,
      allergies: false
    });
    const classes = ref([]);

    // Fonctions pour la sévérité
    const severityColor = (severity) => {
      return {
        'LOW': 'text-green-600',
        'MEDIUM': 'text-yellow-600',
        'HIGH': 'text-orange-600',
        'CRITICAL': 'text-red-600'
      }[severity] || 'text-gray-600';
    };

    const translateSeverity = (severity) => {
      return {
        'LOW': 'Faible',
        'MEDIUM': 'Moyenne',
        'HIGH': 'Élevée',
        'CRITICAL': 'Critique'
      }[severity] || 'Inconnue';
    };

    const openAddAllergyModal = () => {
      showAddAllergyModal.value = true;
    };

    const closeAddAllergyModal = () => {
      showAddAllergyModal.value = false;
    };

    const isProfileComplete = () => {
      const complete = (
        parentData.value &&
        parentData.value.user &&
        parentData.value.user.first_name &&
        parentData.value.user.last_name &&
        parentData.value.address &&
        parentData.value.phone_number
      );
      console.log('Profil complet:', complete);
      return complete;
    };

    const checkFirstLogin = async () => {
      console.log('Vérification de la première connexion...');
      if (!isProfileComplete()) {
        console.log('Profil incomplet, affichage de la modale de bienvenue.');
        setTimeout(() => {
          showWelcomeModal.value = true;
          console.log('Modale de bienvenue affichée:', showWelcomeModal.value);
        }, 1500); // Délai de 1.5 secondes pour correspondre à l'animation
      } else {
        console.log('Profil complet, pas besoin d\'afficher la modale.');
      }
    };

    const getParentProfile = async () => {
      try {
        console.log('Récupération du profil parent...');
        const data = await fetchParentProfile();
        parentData.value = data;
        parentId.value = data.id;
        console.log('Profil parent récupéré :', parentData.value);
        checkFirstLogin(); // Appel de la vérification après la récupération du profil
        return data.id;
      } catch (error) {
        console.error('Erreur lors de la récupération du profil :', error);
        return null;
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
      showCreateStudentModal.value = false;
      showAddAllergyModal.value = false;
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

    const openCreateStudentModal = () => {
      console.log('Ouverture de la modale de création d\'élève.');
      showCreateStudentModal.value = true;
    };

    const closeCreateStudentModal = () => {
      console.log('Fermeture de la modale de création d\'élève.');
      showCreateStudentModal.value = false;
    };

    const handleCreateStudent = () => {
      console.log('Élève créé avec succès.');
      fetchData(parentId.value);
    };

    const loadBackgroundImage = () => {
      const img = new Image();
      img.src = logoPath.value;
      img.onload = () => {
        backgroundLoaded.value = true;
      };
    };

    const toggleSection = (section) => {
      sections.value[section] = !sections.value[section];
    };

    const addItem = (section) => {
      console.log(`Ajout d'un élément dans la section: ${section}`);
    };

    const modifyItem = (section) => {
      console.log(`Modification d'un élément dans la section: ${section}`);
    };

    const getInitials = (prenom, nom) => {
      return `${prenom.charAt(0)}.${nom.charAt(0)}`;
    };

    const getClassName = (classId) => {
      const classe = classes.value.find(classe => classe.id === classId);
      return classe ? classe.name : 'Classe inconnue';
    };

    const fetchData = async (parentId) => {
      if (!parentId) {
        console.warn('Parent ID is not available yet.');
        return;
      }
      try {
        // Récupération réelle des étudiants
        const studentsResponse = await fetchStudentsByParent(parentId);
        enfants.value = studentsResponse.map(student => ({
          id: student.id,
          nom: student.last_name,
          prenom: student.first_name,
          classe: student.grade,
          inscrit_cantine: student.inscrit_cantine
        }));

        // Récupération des allergies
        allergies.value = [];
        for (const student of studentsResponse) {
          const studentAllergies = await fetchStudentAllergies(student.id);
          allergies.value.push(...studentAllergies.map(allergy => ({
            id: allergy.id,
            enfant: `${student.first_name} ${student.last_name}`,
            type: allergy.name,
            description: allergy.description,
            severity: allergy.severity
          })));
        }

        students.value = studentsResponse;

      } catch (error) {
        console.error('Erreur lors de la récupération des données:', error);
      }
    };

    const handleAllergyCreated = () => {
      fetchData(parentId.value);
    };

    onBeforeMount(async () => {
      loadBackgroundImage();
      const id = await getParentProfile();
      if (id) {
        fetchData(id);
      }
    });

    onMounted(async () => {
      // Récupération des classes
      try {
        const classesData = await fetchClasses();
        classes.value = classesData;
      } catch (error) {
        console.error("Erreur lors de la récupération des classes:", error);
      }
      const hideNavbar = () => {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
          navbar.style.display = 'none';
        }
      };

      const showNavbar = () => {
        const navbar = document.querySelector('.navbar');
        if (navbar) {
          navbar.style.display = 'block';
        }
      };

      hideNavbar();

      return () => {
        showNavbar();
      };
    });

    return {
      showWelcomeModal,
      showProfileModal,
      showCreateStudentModal,
      showAddAllergyModal,
      parentData,
      parentId,
      logoPath,
      backgroundLoaded,
      enfants,
      responsables,
      justificatifs,
      allergies,
      students,
      sections,
      classes,
      updateProfile,
      openProfileModal,
      closeProfileModal,
      goToUpdateProfile,
      logoutUser,
      openCreateStudentModal,
      closeCreateStudentModal,
      handleCreateStudent,
      openAddAllergyModal,
      closeAddAllergyModal,
      handleAllergyCreated,
      getInitials,
      toggleSection,
      addItem,
      modifyItem,
      getClassName,
      severityColor,
      translateSeverity
    };
  }
}
</script>

<style scoped>
.dashboard-page {
  min-height: 100vh;
  width: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
  padding: 1rem;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(232, 245, 233, 0.8);
  opacity: 0;
  transition: opacity 1.5s ease;
}

.overlay.fade-in {
  opacity: 1;
}

.content-container {
  position: relative;
  z-index: 10;
}

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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  /* Assurez-vous que ce z-index est suffisamment élevé */
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  z-index: 1001;
  /* Assurez-vous que ce z-index est plus élevé que l'overlay */
}
</style>
