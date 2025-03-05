<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Compléter votre profil</h2>
      <form @submit.prevent="submitForm">
        <input v-model="form.user.first_name" placeholder="Prénom" required>
        <input v-model="form.user.last_name" placeholder="Nom" required>
        <input v-model="form.address.address_line_1" placeholder="Adresse ligne 1" required>
        <input v-model="form.address.address_line_2" placeholder="Adresse ligne 2 (facultatif)">
        <input v-model="form.address.postal_code" placeholder="Code postal" required>
        <input v-model="form.address.city" placeholder="Ville" required>
        <input v-model="form.address.country" placeholder="Pays" required>
        <vue-tel-input v-model="form.phone_number"
          :default-country="'FR'"
          :preferred-countries="['FR', 'CH']"
          :valid-characters-only="true" mode="international"
          :dropdown-options="{ showFlags: true, showDialCodeInList: true, showSearchBox: true }"
          :input-options="{ showDialCode: true, placeholder: 'Entrez votre numéro' }"
          @validate="validatePhone"></vue-tel-input>
        <input v-model="form.relation" placeholder="Relation avec l'enfant (facultatif)">
        <button type="submit">Sauvegarder</button>
      </form>
      <p v-if="notice" class="notice">{{ notice }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { VueTelInput } from 'vue-tel-input';
import 'vue-tel-input/vue-tel-input.css';


const props = defineProps(['parentData']);
const emit = defineEmits(['save', 'close']);

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
    last_name: ''
  }
});

const isValid = ref(false);
const notice = ref(null);

watch(() => props.parentData, (newData) => {
  if (newData) {
    form.value = {
      phone_number: newData.phone_number || '',
      relation: newData.relation || '',
      address: {
        address_line_1: newData.address?.address_line_1 || '',
        address_line_2: newData.address?.address_line_2 || '',
        postal_code: newData.address?.postal_code || '',
        city: newData.address?.city || '',
        country: newData.address?.country || '',
      },
      user: {
        first_name: newData.user?.first_name || '',
        last_name: newData.user?.last_name || ''
      }
    };
  }
}, { immediate: true });

const validatePhone = (isValidNumber) => {
  isValid.value = isValidNumber;
  if (!isValidNumber) {
    notice.value = 'Erreur : Numéro invalide';
  } else {
    notice.value = '';
  }
};

const submitForm = () => {
  if (isValid.value) {
    const formData = {
      phone_number: form.value.phone_number.trim(),
      relation: form.value.relation.trim(),
      address: {
        address_line_1: form.value.address.address_line_1.trim(),
        address_line_2: form.value.address.address_line_2.trim(),
        city: form.value.address.city.trim(),
        postal_code: form.value.address.postal_code.trim(),
        country: form.value.address.country.trim()
      },
      user: {
        first_name: form.value.user.first_name.trim(),
        last_name: form.value.user.last_name.trim()
      }
    };

    emit('save', formData);
    notice.value = 'Votre profil a été mis à jour avec succès.';
    setTimeout(() => {
      notice.value = '';
      emit('close');
    }, 2000);
  } else {
    notice.value = 'Erreur : Numéro invalide';
  }
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
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

.notice {
  margin-top: 10px;
  color: #4CAF50;
}
</style>
