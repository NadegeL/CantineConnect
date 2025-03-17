<template>
  <div class="fixed inset-0 z-[9999] bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4">
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">Ajouter une allergie/PAI</h2>
      </div>

      <form @submit.prevent="submitForm" class="p-4 space-y-3">
        <!-- Sélection étudiant -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Étudiant <span class="text-red-500">*</span>
          </label>
          <select v-model="form.student_id" required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500">
            <option value="" disabled>Sélectionnez un étudiant</option>
            <option v-for="student in students" :key="student.id" :value="student.id">
              {{ student.first_name }} {{ student.last_name }}
            </option>
          </select>
        </div>

        <!-- Nom allergie -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Nom de l'allergie <span class="text-red-500">*</span>
          </label>
          <input v-model="form.name" type="text" required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500">
        </div>

        <!-- Description -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea v-model="form.description"
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500"></textarea>
        </div>

        <!-- Gravité -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Gravité <span class="text-red-500">*</span>
          </label>
          <select v-model="form.severity" required
            class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500">
            <option value="LOW">Faible</option>
            <option value="MEDIUM">Moyenne</option>
            <option value="HIGH">Élevée</option>
            <option value="CRITICAL">Critique</option>
          </select>
        </div>

        <!-- Message d'erreur -->
        <div v-if="error" class="mt-4 p-3 bg-red-50 text-red-700 rounded-lg text-sm">
          {{ error }}
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-3 pt-6">
          <button type="button" @click="closeModal"
            class="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
            Annuler
          </button>
          <button type="submit"
            class="px-4 py-2 text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
            :disabled="isLoading">
            <span v-if="isLoading">Création en cours...</span>
            <span v-else>Créer</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import api from '@/http-common';

export default {
  props: ['students'],
  emits: ['close', 'created'],
  setup(props, { emit }) {
    const form = ref({
      student_id: null,
      name: '',
      description: '',
      severity: 'MEDIUM'
    });

    const isLoading = ref(false);
    const error = ref(null);

    const submitForm = async () => {
      isLoading.value = true;
      try {
        // Validation
        if (!form.value.student_id || !form.value.name) {
          throw new Error('Tous les champs obligatoires doivent être remplis');
        }

        // Appel API
        await api.post(`students/${form.value.student_id}/allergies/create/`, {
          json: {
            name: form.value.name,
            description: form.value.description,
            severity: form.value.severity
          }
        });

        emit('created');
        emit('close');
      } catch (err) {
        error.value = err.message;
      } finally {
        isLoading.value = false;
      }
    };

    const closeModal = () => {
      emit('close');
    };

    return {
      form,
      isLoading,
      error,
      submitForm,
      closeModal
    };
  }
};
</script>


<style scoped>
/* Styles de base */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.5rem rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

/* Formulaire */
.label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.3rem;
  color: #374151;
}

.input,
.select {
  padding: 0.5rem;
  border: 1px solid #D1D5DB;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  color: #374151;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
}

.input:focus,
.select:focus {
  border-color: #3B82F6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
}

.required {
  color: #EF4444;
}

/* Boutons */
.btn-primary,
.btn-secondary {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 600;
  transition: background-color 0.2s;
  cursor: pointer;
  border: none;
  font-size: 0.9rem;
}

.btn-primary {
  background-color: #16A34A;
  color: white;
}

.btn-primary:hover {
  background-color: #15803D;
}

.btn-primary:disabled {
  background-color: #9CA3AF;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: #D1D5DB;
  color: #374151;
}

.btn-secondary:hover {
  background-color: #9CA3AF;
}

.error-message {
  margin-top: 0.5rem;
  padding: 0.5rem;
  background-color: #FEE2E2;
  color: #B91C1C;
  border-radius: 0.375rem;
}
</style>
