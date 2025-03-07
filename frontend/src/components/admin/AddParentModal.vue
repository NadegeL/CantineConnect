<template>
  <div v-if="isVisible" class="modal-overlay">
    <div class="modal">
      <button class="close-modal-btn" @click="closeModal">✖</button>
      <h2>Ajouter un parent</h2>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="parent.email" placeholder="Entrez l'email du parent" required
            class="input-field" />
        </div>
        <div class="form-group">
          <label for="password">Mot de passe temporaire</label>
          <div class="password-field">
            <input :type="passwordVisible ? 'text' : 'password'" id="password" v-model="parent.password"
              placeholder="Entrez un mot de passe" required class="input-field" />
            <button type="button" @click="togglePasswordVisibility" class="toggle-password">
              {{ passwordVisible ? 'Cacher' : 'Afficher' }}
            </button>
          </div>
        </div>
        <div class="form-actions">
          <button type="button" @click="generatePassword" class="generate-btn">Générer un mot de passe</button>
          <button type="submit" class="submit-btn">Créer</button>
        </div>
      </form>

      <div v-if="showConfirmation" class="confirmation-message">
        <p>Le parent a bien été créé !</p>
      </div>

      <div v-if="errorMessage" class="error-message">
        <p>{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import ky from 'ky';

export default {
  props: {
    isVisible: {
      type: Boolean,
      required: true,
    },
    closeModal: {
      type: Function,
      required: true,
    }
  },
  data() {
    return {
      parent: {
        email: '',
        password: '',
      },
      passwordVisible: false,  // Flag pour basculer l'affichage du mot de passe
      showConfirmation: false,  // Flag pour afficher le message de confirmation
      errorMessage: '',  // Variable pour afficher le message d'erreur
    };
  },
  watch: {
    // Lorsque la modale devient visible, réinitialiser les champs
    isVisible(newVal) {
      if (newVal) {
        this.resetForm();  // Réinitialiser les champs à chaque ouverture de la modale
      }
    },
  },
  methods: {
    // Fonction pour basculer la visibilité du mot de passe
    togglePasswordVisibility() {
      this.passwordVisible = !this.passwordVisible;
    },
    // Fonction pour générer un mot de passe temporaire
    generatePassword() {
      // Génère un mot de passe temporaire simple
      this.parent.password = Math.random().toString(36).slice(-8);
    },
    // Fonction de soumission du formulaire
    async handleSubmit() {
      try {
        // Envoi de la requête pour créer le parent
        const response = await ky.post('http://localhost:8000/api/register/', {
          json: {
            email: this.parent.email,
            password: this.parent.password,
            user_type: 'parent',
          },
        });

        if (response.ok) {
          this.showConfirmation = true;  // Affiche le message de confirmation
          setTimeout(() => {
            this.closeModal();  // Ferme la modale après 3 secondes
          }, 3000);

          this.resetForm();  // Réinitialiser le formulaire après succès
          this.errorMessage = '';  // Réinitialise le message d'erreur
        } else {
          // Affiche une erreur détaillée si la réponse n'est pas ok
          const errorData = await response.json();
          this.errorMessage = errorData.detail || 'Une erreur est survenue lors de la création du parent.';
        }
      } catch (error) {
        console.error('Erreur:', error);
        this.errorMessage = 'Une erreur est survenue. Veuillez réessayer plus tard.';
      }
    },
    // Méthode pour réinitialiser les champs du formulaire
    resetForm() {
      this.parent.email = '';
      this.parent.password = '';
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #d8caae;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;
}

.close-modal-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #2e5626;
}

h2 {
  color: #2e5626;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #2e5626;
}

.input-field {
  width: 100%;
  padding: 8px;
  border: 1px solid #E3E3E3;
  border-radius: 4px;
  box-sizing: border-box;
  height: 40px;
}

.password-field {
  display: flex;
}

.toggle-password {
  background-color: #2e5626;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 0 4px 4px 0;
}

.form-actions button {
  width: 100%;
  padding: 10px;
  margin-top: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.generate-btn {
  background-color: #4a7b2a;
  color: white;
}

.submit-btn {
  background-color: #2e5626;
  color: white;
}

.submit-btn:hover,
.generate-btn:hover {
  background-color: #4a7b2a;
}

.confirmation-message {
  margin-top: 20px;
  color: #2e5626;
  font-weight: bold;
  text-align: center;
}

.error-message {
  margin-top: 20px;
  color: #d9534f;
  font-weight: bold;
  text-align: center;
}
</style>
