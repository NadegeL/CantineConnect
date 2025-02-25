<template>
  <div class="create-admin">
    <h1>{{ isInitialCreation ? 'Créer un Administrateur' : 'Ajouter un Administrateur' }}</h1>
    <form @submit.prevent="createAdmin">
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

      <button type="submit" class="submit-btn">{{ isInitialCreation ? 'Créer l\'administrateur' : 'Ajouter l\'administrateur' }}</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
import api from '@/http-common';
import { checkAdminExists } from '@/router';

export default {
  name: 'CreateAdmin',
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
      isInitialCreation: false,
    };
  },
  async created() {
    await this.fetchSchoolZones();
    this.isInitialCreation = this.$route.name === 'CreateAdmin';
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
    async createAdmin() {
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

        this.successMessage = this.isInitialCreation
          ? "L'administrateur a été créé avec succès. Redirection vers la page de connexion..."
          : "L'administrateur a été ajouté avec succès.";

        // Invalider le cache
        checkAdminExists.invalidateCache();

        setTimeout(() => {
          this.$router.push(this.isInitialCreation ? '/admin/login' : '/admin').catch(() => {
            this.errorMessage = "Erreur lors de la redirection. Veuillez vous connecter manuellement.";
          });
        }, 3000);
      } catch (error) {
        console.error('Error creating admin:', error);
        this.errorMessage = "Erreur lors de la création de l'administrateur. Veuillez réessayer.";
      }
    },
  },
};
</script>

<style scoped>
.create-admin {
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
