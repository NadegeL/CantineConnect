<template>
  <div class="add-admin">
    <h1>Ajouter un Administrateur</h1>
    <form @submit.prevent="addAdmin">
      <h2>Informations utilisateur</h2>
      <input v-model="userData.email" type="email" placeholder="Email" required />
      <input v-model="userData.password" type="password" placeholder="Mot de passe" required />
      <input v-model="passwordConfirmation" type="password" placeholder="Confirmer le mot de passe" required />
      <input v-model="userData.first_name" placeholder="Prénom" required />
      <input v-model="userData.last_name" placeholder="Nom" required />

      <h2>Adresse</h2>
      <input v-model="addressData.address_line_1" placeholder="Adresse ligne 1" required />
      <input v-model="addressData.address_line_2" placeholder="Adresse ligne 2" />
      <input v-model="addressData.postal_code" placeholder="Code postal" required />
      <input v-model="addressData.city" placeholder="Ville" required />
      <input v-model="addressData.country" placeholder="Pays" required />

      <h2>Zone académique</h2>
      <label for="zone-select">Zone académique</label>
      <select v-model="adminData.zone" id="zone-select" required>
        <option v-for="zone in schoolZones" :key="zone.id" :value="zone.name">
          {{ zone.name }}
        </option>
      </select>

      <button type="submit" class="submit-btn">Ajouter l'administrateur</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
import api from '@/http-common';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'AddAdmin',
  data() {
    return {
      userData: {
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        user_type: 'school_admin',
      },
      passwordConfirmation: '',
      addressData: {
        address_line_1: '',
        address_line_2: '',
        postal_code: '',
        city: '',
        country: '',
      },
      adminData: {
        zone: '',
        invoice_edited: false,
      },
      schoolZones: [],
      errorMessage: '',
      successMessage: '',
    };
  },
  async created() {
    const authStore = useAuthStore();
    if (!authStore.isAuthenticated || authStore.userGroup !== 'school_admin') {
      this.$router.push('/admin/login');
      return;
    }
    await this.fetchSchoolZones();
  },
  methods: {
    async fetchSchoolZones() {
      try {
        const response = await api.get('school-zones/').json();
        this.schoolZones = response;
      } catch (error) {
        this.errorMessage = 'Erreur lors de la récupération des zones scolaires.';
      }
    },
    async addAdmin() {
      if (this.userData.password !== this.passwordConfirmation) {
        this.errorMessage = "Les mots de passe ne correspondent pas.";
        return;
      }

      try {
        this.errorMessage = '';
        this.successMessage = '';

        const requestData = {
          email: this.userData.email,
          password: this.userData.password,
          first_name: this.userData.first_name,
          last_name: this.userData.last_name,
          user_type: this.userData.user_type,
          address: this.addressData,
          administration: {
            zone: this.adminData.zone,
            invoice_edited: this.adminData.invoice_edited,
          },
        };

        await api.post('register/', { json: requestData }).json();

        this.successMessage = "L'administrateur a été ajouté avec succès.";
        this.resetForm();
      } catch (error) {
        console.error('Error adding admin:', error);
        this.errorMessage = "Erreur lors de l'ajout de l'administrateur. Veuillez réessayer.";
      }
    },
    resetForm() {
      this.userData = {
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        user_type: 'school_admin',
      };
      this.passwordConfirmation = '';
      this.addressData = {
        address_line_1: '',
        address_line_2: '',
        postal_code: '',
        city: '',
        country: '',
      };
      this.adminData = {
        zone: '',
        invoice_edited: false,
      };
    },
  },
};
</script>

<style scoped>
.add-admin {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  color: #436F8A;
}

input, select {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #E3E3E3;
  border-radius: 4px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #FFB347;
  color: #FFFFFF;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #FFA500;
}

.error-message {
  color: #FF6F61;
  margin-top: 10px;
}

.success-message {
  color: #3A6351;
  margin-top: 10px;
  font-weight: bold;
}
</style>
