<template>
  <div class="fixed inset-0 z-[9999] bg-black bg-opacity-50 flex items-center justify-center">
    <div class="modal-content">
      <!-- En-tête -->
      <div class="p-4 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-800">Ajouter un élève</h2>
      </div>

      <!-- Corps du formulaire -->
      <form @submit.prevent="submitForm" class="p-4 space-y-3">
        <!-- Prénom -->
        <div>
          <label class="label">
            Prénom <span class="required">*</span>
          </label>
          <input v-model="form.first_name" type="text" required class="input">
        </div>

        <!-- Nom -->
        <div>
          <label class="label">
            Nom <span class="required">*</span>
          </label>
          <input v-model="form.last_name" type="text" required class="input">
        </div>

        <!-- Date de naissance -->
        <div>
          <label class="label">
            Date de naissance <span class="required">*</span>
          </label>
          <input v-model="form.birth_date" type="date" required class="input">
        </div>

        <!-- Classe -->
        <div>
          <label class="label">
            Classe <span class="required">*</span>
          </label>
          <select v-model="form.class_id" required class="select">
            <option value="" disabled>Sélectionnez une classe</option>
            <option v-for="classe in classes" :key="classe.id" :value="classe.id">
              {{ classe.name }}
            </option>
          </select>
        </div>

        <!-- Message d'erreur -->
        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-2 pt-4">
          <button type="button" @click="closeModal" class="btn-secondary">
            Annuler
          </button>
          <button type="submit" class="btn-primary" :disabled="isLoading">
            <span v-if="isLoading">Création...</span>
            <span v-else>Créer</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { fetchClasses, createStudentWithParent } from '@/services/studentService';

export default {
  props: {
    parentId: {
      type: Number,
      required: true
    }
  },
  emits: ['close', 'created'],
  setup(props, { emit }) {
    const form = ref({
      first_name: '',
      last_name: '',
      birth_date: '',
      class_id: null
    });

    const classes = ref([]);
    const isLoading = ref(false);
    const error = ref(null);

    const loadClasses = async () => {
      try {
        classes.value = await fetchClasses();
      } catch (err) {
        error.value = "Erreur lors du chargement des classes";
      }
    };

    const submitForm = async () => {
      isLoading.value = true;
      error.value = null;

      try {
        const selectedClasse = classes.value.find(c => c.id === form.value.class_id);
        if (!selectedClasse) {
          throw new Error('Veuillez sélectionner une classe valide');
        }
        if (!form.value.first_name?.trim() ||
          !form.value.last_name?.trim() ||
          !form.value.birth_date ||
          !form.value.class_id) {
          throw new Error('Tous les champs obligatoires doivent être remplis');
        }

        if (!/^\d{4}-\d{2}-\d{2}$/.test(form.value.birth_date)) {
          throw new Error('Format de date invalide (AAAA-MM-JJ requis)');
        }

        const payload = {
          first_name: form.value.first_name.trim(),
          last_name: form.value.last_name.trim(),
          birth_date: form.value.birth_date,
          grade: selectedClasse.id,  // Utilisez form.class_id pour grade
          parents: [props.parentId],
          allergies: []  // Incluez les allergies si nécessaire
        };

        console.log("Payload envoyé:", payload);  // Ajoutez ce log pour vérifier le payload

        await createStudentWithParent(payload, props.parentId);
        emit('created');
        closeModal();
      } catch (err) {
        console.error("Error caught in submitForm:", err); // Log the error
        error.value = err.message || "Erreur lors de la création";
        console.error("Erreur API:", err.response?.data);
      } finally {
        isLoading.value = false;
      }
    };

    const closeModal = () => {
      emit('close');
    };

    onMounted(loadClasses);

    return {
      form,
      classes,
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
