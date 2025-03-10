<template>
  <div class="update-profile">
    <h1>Mettre à jour votre profil</h1>

    <div class="tabs">
      <button :class="{ active: activeTab === 'parent' }" @click="switchTab('parent')">Profil Parent</button>
      <button v-for="(student, index) in students" :key="student.id"
        :class="{ active: activeTab === `student-${index}` }" @click="switchTab(`student-${index}`)">
        {{ student.first_name }}
      </button>
    </div>

    <div v-if="activeTab === 'parent'">
      <form @submit.prevent="submitParentForm">
        <div class="form-group">
          <label for="first_name">Prénom</label>
          <input id="first_name" v-model="form.user.first_name" placeholder="Prénom" required>
        </div>

        <div class="form-group">
          <label for="last_name">Nom</label>
          <input id="last_name" v-model="form.user.last_name" placeholder="Nom" required>
        </div>

        <div class="form-group">
          <label for="email">Email actuel</label>
          <input id="email" v-model="form.user.email" type="email" disabled>
        </div>

        <div class="form-group">
          <label for="new_email">Nouvel email (laisser vide si inchangé)</label>
          <input id="new_email" v-model="form.user.new_email" type="email" placeholder="Nouveau email">
        </div>
        <div class="form-group">
          <label for="new_password">Nouveau mot de passe</label>
          <input id="new_password" v-model="form.new_password" type="password" @input="validatePasswordsMatch"
            placeholder="Nouveau mot de passe (laisser vide si inchangé)">
        </div>

        <div class="form-group">
          <label for="confirm_password">Confirmer le nouveau mot de passe</label>
          <input id="confirm_password" v-model="form.confirm_password" type="password" @input="validatePasswordsMatch"
            placeholder="Confirmer le nouveau mot de passe">
        </div>

        <p v-if="isError" class="error-message">{{ notice }}</p>

        <div class="form-group">
          <label for="address_line_1">Adresse ligne 1</label>
          <input id="address_line_1" v-model="form.address.address_line_1" placeholder="Adresse ligne 1" required>
        </div>

        <div class="form-group">
          <label for="address_line_2">Adresse ligne 2</label>
          <input id="address_line_2" v-model="form.address.address_line_2" placeholder="Adresse ligne 2 (facultatif)">
        </div>

        <div class="form-group">
          <label for="postal_code">Code postal</label>
          <input id="postal_code" v-model="form.address.postal_code" placeholder="Code postal" required>
        </div>

        <div class="form-group">
          <label for="city">Ville</label>
          <input id="city" v-model="form.address.city" placeholder="Ville" required>
        </div>

        <div class="form-group">
          <label for="country">Pays</label>
          <input id="country" v-model="form.address.country" placeholder="Pays" required>
        </div>

        <div class="form-group">
          <label for="phone_number">Numéro de téléphone</label>
          <vue-tel-input v-model="form.phone_number" :default-country="'FR'" :preferred-countries="['FR', 'CH']"
            :valid-characters-only="true" mode="international"
            :dropdown-options="{ showFlags: true, showDialCodeInList: true, showSearchBox: true }"
            :input-options="{ showDialCode: true, placeholder: 'Entrez votre numéro' }"
            @validate="validatePhone"></vue-tel-input>
        </div>

        <div class="form-group">
          <label for="relation">Relation avec l'enfant</label>
          <input id="relation" v-model="form.relation" placeholder="Relation avec l'enfant (facultatif)">
        </div>

        <button type="submit" :disabled="isSubmitting || isError">Valider le profil parent</button>
      </form>
    </div>

    <div v-for="(student, index) in students" :key="student.id" v-show="activeTab === `student-${index}`">
      <form @submit.prevent="submitStudentForm(student.id)">
        <div class="form-group">
          <label :for="`student-first-name-${index}`">Prénom de l'élève</label>
          <input :id="`student-first-name-${index}`" v-model="student.first_name" required>
        </div>
        <div class="form-group">
          <label :for="`student-last-name-${index}`">Nom de l'élève</label>
          <input :id="`student-last-name-${index}`" v-model="student.last_name" required>
        </div>
        <div class="form-group">
          <label :for="`student-birth-date-${index}`">Date de naissance</label>
          <input :id="`student-birth-date-${index}`" v-model="student.birth_date" type="date" required>
        </div>
        <div class="form-group">
          <label :for="`student-grade-${index}`">Classe</label>
          <select :id="`student-grade-${index}`" v-model="student.grade" required>
            <option v-for="classe in classes" :key="classe.id" :value="classe.id">{{ classe.name }}</option>
          </select>
        </div>
        <div class="form-group">
          <label>Allergies</label>
          <ul>
            <li v-for="allergy in student.allergies" :key="allergy.id">
              {{ allergy.name }}
              <button type="button" @click="openAllergyModal(allergy)">Éditer</button>
              <button type="button" @click="deleteStudentAllergyLocal(student.id, allergy.id)">Supprimer</button>
            </li>
          </ul>
        </div>
        <button type="submit" :disabled="isSubmitting || isError">Valider le profil de l'élève</button>
      </form>
    </div>

    <!-- Modale pour éditer les allergies -->
    <div v-if="showAllergyModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeAllergyModal">&times;</span>
        <h2>Éditer l'allergie</h2>
        <form @submit.prevent="updateAllergy">
          <div class="form-group">
            <label for="allergy-name">Nom de l'allergie</label>
            <input id="allergy-name" v-model="selectedAllergy.name" required>
          </div>
          <div class="form-group">
            <label for="allergy-description">Description</label>
            <textarea id="allergy-description" v-model="selectedAllergy.description"></textarea>
          </div>
          <div class="form-group">
            <label for="allergy-severity">Sévérité</label>
            <select id="allergy-severity" v-model="selectedAllergy.severity" required>
              <option value="LOW">Faible</option>
              <option value="MEDIUM">Moyen</option>
              <option value="HIGH">Élevé</option>
              <option value="CRITICAL">Critique</option>
            </select>
          </div>
          <button type="submit">Mettre à jour l'allergie</button>
        </form>
      </div>
    </div>

    <div class="actions">
      <button @click="goBack" class="btn-back">Retour au tableau de bord</button>
    </div>

    <p v-if="notice" class="notice" :class="{ 'error': isError }">{{ notice }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { fetchParentProfile, saveProfile, validatePhone as validatePhoneNumber } from '@/services/parentService';
import { validatePassword as validateUserPassword } from '@/services/profileService';
import { validateEmail } from '@/services/profileService';
import { fetchStudentsByParent, updateStudent, fetchClasses, fetchAllergies, updateStudentAllergy, deleteStudentAllergy } from '@/services/studentService';
import { VueTelInput } from 'vue-tel-input';
import 'vue-tel-input/vue-tel-input.css';

const router = useRouter();
const form = ref({
  phone_number: '',
  relation: '',
  address: {
    address_line_1: '',
    address_line_2: '',
    postal_code: '',
    city: '',
    country: '',
  },
  user: {
    first_name: '',
    last_name: '',
    email: '',
    new_email: ''
  },
  new_password: '',
  confirm_password: ''
});
const students = ref([]);
const classes = ref([]);
const allergiesList = ref([]);
const activeTab = ref('parent');
const isValid = ref(false);
const notice = ref(null);
const isError = ref(false);
const isSubmitting = ref(false);
const hasUnsavedChanges = ref(false);
const showAllergyModal = ref(false);
const selectedAllergy = ref({ name: '', description: '', severity: 'LOW' });

const validatePhone = (isValidNumber) => {
  isValid.value = isValidNumber;
  if (!isValidNumber) {
    notice.value = 'Erreur : Numéro invalide';
    isError.value = true;
  } else {
    notice.value = '';
    isError.value = false;
  }
};

const fetchProfile = async () => {
  try {
    const profileData = await fetchParentProfile();
    form.value = {
      phone_number: profileData.phone_number || '',
      relation: profileData.relation || '',
      address: {
        address_line_1: profileData.address?.address_line_1 || '',
        address_line_2: profileData.address?.address_line_2 || '',
        postal_code: profileData.address?.postal_code || '',
        city: profileData.address?.city || '',
        country: profileData.address?.country || '',
      },
      user: {
        id: profileData.id,
        first_name: profileData.user?.first_name || '',
        last_name: profileData.user?.last_name || '',
        email: profileData.user?.email || '',
        new_email: ''
      },
      new_password: '',
      confirm_password: ''
    };
  } catch (error) {
    console.error('Erreur lors de la récupération du profil:', error);
    notice.value = 'Erreur lors de la récupération du profil.';
    isError.value = true;
  }
};

const fetchAllData = async (parentId) => {
  try {
    const [studentsData, classesData, allergiesData] = await Promise.all([
      fetchStudentsByParent(parentId),
      fetchClasses(),
      fetchAllergies()
    ]);

    students.value = studentsData;
    classes.value = classesData;
    allergiesList.value = allergiesData;
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
    notice.value = 'Erreur lors de la récupération des données.';
    isError.value = true;
  }
};

const validatePasswordsMatch = () => {
  if (form.value.new_password !== form.value.confirm_password) {
    notice.value = 'Erreur : Les mots de passe ne correspondent pas.';
    isError.value = true;
  } else {
    notice.value = '';
    isError.value = false;
  }
};

const submitParentForm = async () => {
  isError.value = false;
  notice.value = '';

  if (!isValid.value) {
    notice.value = 'Erreur : Numéro de téléphone invalide';
    isError.value = true;
    return;
  }

  if (form.value.user.new_email && !validateEmail(form.value.user.new_email)) {
    notice.value = 'Erreur : L\'adresse email n\'est pas valide.';
    isError.value = true;
    return;
  }

  if (form.value.new_password || form.value.confirm_password) {
    if (form.value.new_password !== form.value.confirm_password) {
      notice.value = 'Erreur : Les mots de passe ne correspondent pas.';
      isError.value = true;
      return;
    }
    const passwordValidation = validateUserPassword(form.value.new_password);
    if (!passwordValidation) {
      notice.value = `Erreur : Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.`;
      isError.value = true;
      return;
    }
  }

  if (isError.value) {
    return;
  }

  isSubmitting.value = true;
  try {
    await saveProfile(form.value);
    notice.value = 'Votre profil a été mis à jour avec succès.';
    isError.value = false;
    hasUnsavedChanges.value = false;
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil:', error);
    notice.value = 'Erreur lors de la mise à jour du profil.';
    isError.value = true;
  } finally {
    isSubmitting.value = false;
  }
};

const submitStudentForm = async (studentId) => {
  try {
    const student = students.value.find(s => s.id === studentId);
    await updateStudent(studentId, student);
    notice.value = `Profil de l'élève ${student.first_name} mis à jour avec succès.`;
    isError.value = false;
    hasUnsavedChanges.value = false;
  } catch (error) {
    console.error(`Erreur lors de la mise à jour du profil de l'élève:`, error);
    notice.value = `Erreur lors de la mise à jour du profil de l'élève.`;
    isError.value = true;
  }
};

const switchTab = (tab) => {
  if (hasUnsavedChanges.value) {
    if (!confirm('Vous avez des modifications non sauvegardées. Voulez-vous vraiment changer d\'onglet ?')) {
      return;
    }
  }
  activeTab.value = tab;
  hasUnsavedChanges.value = false;
};

const goBack = () => {
  if (hasUnsavedChanges.value) {
    if (!confirm('Vous avez des modifications non sauvegardées. Voulez-vous vraiment quitter ?')) {
      return;
    }
  }
  router.push('/parent-dashboard');
};

const openAllergyModal = (allergy) => {
  selectedAllergy.value = { ...allergy };
  showAllergyModal.value = true;
};

const closeAllergyModal = () => {
  showAllergyModal.value = false;
  selectedAllergy.value = { name: '', description: '', severity: 'LOW' };
};

const updateAllergy = async () => {
  try {
    await updateStudentAllergy(selectedAllergy.value);
    closeAllergyModal();
    notice.value = 'Allergie mise à jour avec succès.';
    isError.value = false;
  } catch (error) {
    console.error('Erreur lors de la mise à jour de l\'allergie:', error);
    notice.value = 'Erreur lors de la mise à jour de l\'allergie.';
    isError.value = true;
  }
};

const deleteStudentAllergyLocal = async (studentId, allergyId) => {
  if (confirm('Voulez-vous vraiment supprimer cette allergie ?')) {
    try {
      await deleteStudentAllergy(studentId, allergyId);
      notice.value = 'Allergie supprimée avec succès.';
      isError.value = false;
      // Mettre à jour la liste des allergies de l'étudiant
      const student = students.value.find(s => s.id === studentId);
      student.allergies = student.allergies.filter(a => a.id !== allergyId);
    } catch (error) {
      console.error('Erreur lors de la suppression de l\'allergie:', error);
      notice.value = 'Erreur lors de la suppression de l\'allergie.';
      isError.value = true;
    }
  }
};

onMounted(async () => {
  try {
    await fetchProfile();
    if (form.value.user && form.value.user.id) {
      const parentId = form.value.user.id;
      await fetchAllData(parentId);
    } else {
      console.error("L'ID du parent n'est pas défini.");
      // Gérez le cas où l'ID du parent est manquant
      notice.value = 'Erreur : L\'ID du parent n\'est pas défini.';
      isError.value = true;
    }
  } catch (error) {
    console.error('Erreur lors de la récupération des données:', error);
    notice.value = 'Erreur lors de la récupération des données.';
    isError.value = true;
  }
});
</script>


<style scoped>
.update-profile {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input,
.vue-tel-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.btn-back {
  background-color: #f44336;
  margin-top: 10px;
}

.notice {
  margin-top: 10px;
  padding: 10px;
  border-radius: 4px;
}

.notice.error {
  background-color: #ffebee;
  color: #c62828;
}

.tabs {
  display: flex;
  margin-bottom: 20px;
}

.tabs button {
  padding: 10px 15px;
  margin-right: 5px;
  border: none;
  background-color: #82828255;
  cursor: pointer;
}

.tabs button.active {
  background-color: #4CAF50;
  color: white;
}

.actions {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
}

.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 100%;
  max-width: 400px;
}

.close {
  float: right;
  font-size: 20px;
  cursor: pointer;
}
</style>
