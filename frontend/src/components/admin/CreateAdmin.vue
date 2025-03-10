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
      <select v-model="adminData.zone" 
              id="zone-select" 
              required
              class="zone-select">
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
  background-color: #d8caae;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1, h2 {
  color: #2e5626;
}

input, select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ebe1d0;
  border-radius: 4px;
  box-sizing: border-box;
  height: 40px;
  font-size: 16px;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #2e5626;
  color: #FFFFFF;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  height: 40px;
}

.submit-btn:hover {
  background-color: #4a7b2a;
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

select:focus {
  outline-color: #2e5626;
  box-shadow: 0 0 0 1px #2e5626;
}

select option:checked,
select option:hover,
select option:focus {
  background-color: #2e5626;
  color: #ebe1d0;
}

.zone-select {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ebe1d0;
  border-radius: 4px;
  height: 40px;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 12 12'%3E%3Cpath d='M1 4l5 5 5-5z' fill='%232e5626'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  padding-right: 30px;
  font-size: 16px;
}

.zone-select:focus {
  outline: none;
  border-bottom: #2e5626;
  box-shadow: 0 0 0 1px #2e5626;
}
</style>
