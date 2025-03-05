<template>
  <div class="update-profile">
    <h1>Mettre à jour votre profil</h1>
    <form @submit.prevent="submitForm">
      <input v-model="form.user.first_name" placeholder="Prénom" required>
      <input v-model="form.user.last_name" placeholder="Nom" required>
      <input v-model="form.user.email" type="email" placeholder="Email" required>
      <input v-model="form.address.address_line_1" placeholder="Adresse ligne 1" required>
      <input v-model="form.address.address_line_2" placeholder="Adresse ligne 2 (facultatif)">
      <input v-model="form.address.postal_code" placeholder="Code postal" required>
      <input v-model="form.address.city" placeholder="Ville" required>
      <input v-model="form.address.country" placeholder="Pays" required>
      <vue-tel-input v-model="form.phone_number" :default-country="'FR'" :preferred-countries="['FR', 'CH']"
        :valid-characters-only="true" mode="international"
        :dropdown-options="{ showFlags: true, showDialCodeInList: true }"
        :input-options="{ showDialCode: true, placeholder: 'Entrez votre numéro' }"
        @validate="validatePhone"></vue-tel-input>
      <input v-model="form.relation" placeholder="Relation avec l'enfant (facultatif)">
      <input v-model="form.new_password" type="password" placeholder="Nouveau mot de passe (laisser vide si inchangé)">
      <button type="submit">Sauvegarder</button>
    </form>
    <button @click="goBack" class="btn-back">Retour au tableau de bord</button>
    <p v-if="notice" class="notice">{{ notice }}</p>
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
    email: ''
  },
  new_password: ''
});

const isValid = ref(false);
const notice = ref(null);

const validatePhone = (isValidNumber) => {
  isValid.value = isValidNumber;
  if (!isValidNumber) {
    notice.value = 'Erreur : Numéro invalide';
  } else {
    notice.value = '';
  }
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
        email: data.user?.email || ''
      },
      new_password: ''
    };
  } catch (error) {
    console.error('Erreur lors de la récupération du profil:', error);
    notice.value = 'Erreur lors de la récupération des données.';
  }
};

const submitForm = async () => {
  if (isValid.value) {
    try {
      const formData = {
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
          email: form.value.user.email.trim()
        }
      };

      if (form.value.new_password) {
        formData.new_password = form.value.new_password;
      }

      const response = await api.patch('parent/profile/', { json: formData });
      const data = await response.json();
      notice.value = 'Votre profil a été mis à jour avec succès.';

      setTimeout(() => {
        notice.value = '';
        router.push('/parent-dashboard');
      }, 2000);
    } catch (error) {
      console.error('Erreur lors de la mise à jour du profil:', error);
      if (error.response) {
        console.log('Réponse d\'erreur:', error.response.data);
        notice.value = `Erreur : ${JSON.stringify(error.response.data)}`;
      } else {
        notice.value = 'Erreur inconnue lors de la mise à jour.';
      }
    }
  } else {
    notice.value = 'Erreur : Numéro invalide.';
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

form {
  display: flex;
  flex-direction: column;
}

input,
.vue-tel-input,
button {
  margin-bottom: 10px;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
}

.btn-back {
  background-color: #f44336;
}

.notice {
  margin-top: 10px;
}
</style>
