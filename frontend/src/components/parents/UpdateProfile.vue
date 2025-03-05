<template>
  <div class="update-profile">
    <h1>Mettre à jour votre profil</h1>
    <form @submit.prevent="submitForm">
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
        <input id="new_password" v-model="form.new_password" type="password"
          placeholder="Nouveau mot de passe (laisser vide si inchangé)">
      </div>

      <div class="form-group">
        <label for="confirm_password">Confirmer le nouveau mot de passe</label>
        <input id="confirm_password" v-model="form.confirm_password" type="password"
          placeholder="Confirmer le nouveau mot de passe">
      </div>

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
        <vue-tel-input v-model="form.phone_number" :default-country="'FR'"
          :preferred-countries="['FR', 'CH']"
          :valid-characters-only="true" mode="international"
          :dropdown-options="{ showFlags: true, showDialCodeInList: true, showSearchBox: true }"
          :input-options="{ showDialCode: true, placeholder: 'Entrez votre numéro' }"
          @validate="validatePhone"></vue-tel-input>
      </div>

      <div class="form-group">
        <label for="relation">Relation avec l'enfant</label>
        <input id="relation" v-model="form.relation" placeholder="Relation avec l'enfant (facultatif)">
      </div>

      <button type="submit" :disabled="isSubmitting">{{ isSubmitting ? 'Sauvegarde en cours...' : 'Sauvegarder'
        }}</button>
    </form>
    <button @click="goBack" class="btn-back">Retour au tableau de bord</button>
    <p v-if="notice" class="notice" :class="{ 'error': isError }">{{ notice }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/http-common';
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

const isValid = ref(false);
const notice = ref(null);
const isError = ref(false);
const isSubmitting = ref(false);

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

const validatePassword = (password) => {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasNonalphas = /\W/.test(password);
  return password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasNonalphas;
};

const fetchProfile = async () => {
  try {
    const response = await api.get('parent/profile/');
    const data = await response.json();
    form.value = {
      phone_number: data.phone_number || '',
      relation: data.relation || '',
      address: {
        address_line_1: data.address?.address_line_1 || '',
        address_line_2: data.address?.address_line_2 || '',
        postal_code: data.address?.postal_code || '',
        city: data.address?.city || '',
        country: data.address?.country || '',
      },
      user: {
        first_name: data.user?.first_name || '',
        last_name: data.user?.last_name || '',
        email: data.user?.email || '',
        new_email: ''
      },
      new_password: '',
      confirm_password: ''
    };
  } catch (error) {
    console.error('Erreur lors de la récupération du profil:', error);
    notice.value = 'Erreur lors de la récupération des données.';
    isError.value = true;
  }
};

const submitForm = async () => {
  if (!isValid.value) {
    notice.value = 'Erreur : Numéro de téléphone invalide';
    isError.value = true;
    return;
  }

  if (form.value.new_password || form.value.confirm_password) {
    if (form.value.new_password !== form.value.confirm_password) {
      notice.value = 'Erreur : Les mots de passe ne correspondent pas.';
      isError.value = true;
      return;
    }
    if (!validatePassword(form.value.new_password)) {
      notice.value = 'Erreur : Le mot de passe doit contenir au moins 8 caractères, une majuscule, une minuscule, un chiffre et un caractère spécial.';
      isError.value = true;
      return;
    }
  }

  isSubmitting.value = true;
  try {
    const dataToSend = {
      phone_number: form.value.phone_number.trim(),
      relation: form.value.relation.trim(),
      address: {
        address_line_1: form.value.address.address_line_1.trim(),
        address_line_2: form.value.address.address_line_2.trim(),
        postal_code: form.value.address.postal_code.trim(),
        city: form.value.address.city.trim(),
        country: form.value.address.country.trim(),
      },
      user: {
        first_name: form.value.user.first_name.trim(),
        last_name: form.value.user.last_name.trim(),
      }
    };

    if (form.value.user.new_email) {
      dataToSend.user.email = form.value.user.new_email.trim();
    }

    if (form.value.new_password) {
      dataToSend.user.new_password = form.value.new_password;
    }

    const response = await api.patch('parent/profile/', { json: dataToSend });
    const data = await response.json();
    notice.value = 'Votre profil a été mis à jour avec succès.';
    isError.value = false;

    setTimeout(() => {
      notice.value = '';
      router.push('/parent-dashboard');
    }, 2000);
  } catch (error) {
    console.error('Erreur lors de la mise à jour du profil:', error);
    if (error.response) {
      const errorData = await error.response.json();
      console.error('Réponse d\'erreur:', errorData);
      notice.value = `Erreur : ${JSON.stringify(errorData)}`;
    } else {
      notice.value = 'Erreur inconnue lors de la mise à jour.';
    }
    isError.value = true;
  } finally {
    isSubmitting.value = false;
  }
};

const goBack = () => {
  router.push('/parent-dashboard');
};

onMounted(fetchProfile);
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
</style>
