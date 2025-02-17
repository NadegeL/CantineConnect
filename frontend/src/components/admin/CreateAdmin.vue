<template>
  <div class="create-admin">
    <h1>Créer un administrateur</h1>
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
        <option v-for="zone in schoolZones" :key="zone.id" :value="zone.id">
          {{ zone.name }}
        </option>
      </select>

      <button type="submit" class="submit-btn">Créer l'administrateur</button>
    </form>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="successMessage" class="success-message">{{ successMessage }}</div>
  </div>
</template>

<script>
import api from '@/http-common';
import { checkAdminExists } from '@/router'; // Import verification function

export default {
  name: 'CreateAdmin',
  data() {
    return {
      userData: {
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        is_active: true,
        is_staff: true,
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
      },
      schoolZones: [],
      errorMessage: '',
      successMessage: '',
    };
  },
  async created() {
    await this.fetchSchoolZones();
  },
  methods: {
    async fetchSchoolZones() {
      try {
        const response = await api.get('school-zones/').json();
        this.schoolZones = response;
      } catch (error) {
        this.errorMessage = 'Erreur lors de la récupération des zones scolaires.';
        console.error('Erreur lors de la récupération des zones scolaires:', error);
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

        const userResponse = await api.post('users/', {
          json: {
            username: this.userData.email.split('@')[0],
            email: this.userData.email,
            password: this.userData.password,
            first_name: this.userData.first_name,
            last_name: this.userData.last_name,
            is_active: true,
            is_staff: true,
          }
        }).json();

        const userId = userResponse.id;

        const addressResponse = await api.post('addresses/', { json: this.addressData }).json();
        const addressId = addressResponse.id;

        const adminData = {
          user: userId,
          is_admin: true,
          invoice_edited: false,
          address: addressId,
          zone: this.adminData.zone,
        };

        console.log('Données envoyées pour créer l\'administrateur:', adminData);

        await api.post('administrations/', { json: adminData });
        console.log('Administrateur créé avec succès');

        this.successMessage = "L'administrateur a été créé avec succès. Redirection vers la page de connexion...";

        // Rerun administrator existence check
        await checkAdminExists();

        setTimeout(() => {
          this.$router.push('/admin/login').catch(err => {
            console.error('Erreur de redirection:', err);
            this.errorMessage = "Erreur lors de la redirection. Veuillez vous connecter manuellement.";
          });
        }, 3000);
      } catch (error) {
        if (error.response) {
          const errorData = await error.response.json();
          if (errorData.email && errorData.email.includes("already exists")) {
            this.errorMessage = "Cette adresse email est déjà utilisée.";
          } else if (errorData.username && errorData.username.includes("already exists")) {
            this.errorMessage = "Ce nom d'utilisateur existe déjà.";
          } else {
            this.errorMessage = "Données invalides. Vérifiez les informations saisies.";
          }
        } else {
          this.errorMessage = "Erreur inattendue. Veuillez réessayer plus tard.";
        }
        console.error("Erreur lors de la création de l'administrateur :", error);
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
