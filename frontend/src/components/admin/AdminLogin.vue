<template>
  <div class="admin-login">
    <h1>Connexion Administration</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Email</label>
        <input id="username" v-model="username" type="email" required>
      </div>
      <div class="form-group">
        <label for="password">Mot de passe</label>
        <div class="password-input">
          <input id="password" v-model="password" :type="showPassword ? 'text' : 'password'" required>
          <button type="button" @click="togglePasswordVisibility" class="toggle-password">
            {{ showPassword ? 'Cacher' : 'Afficher' }}
          </button>
        </div>
      </div>
      <button type="submit" class="submit-btn" :disabled="isLoading">
        {{ isLoading ? 'Connexion en cours...' : 'Se connecter' }}
      </button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { ROUTE_NAMES } from '@/router';

export default {
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  },
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      isLoading: false,
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        await this.authStore.login(this.username, this.password);

        if (this.authStore.userType === 'school_admin') {
          this.$router.push({ name: ROUTE_NAMES.ADMIN_DASHBOARD }).catch(err => {
            console.error('Redirection error:', err);
          });
        } else {
          throw new Error('Unauthorized user type');
        }
      } catch (error) {
        console.error('Login failed:', error);
        this.errorMessage = "Erreur de connexion. Veuillez vérifier vos identifiants et réessayer.";
      } finally {
        this.isLoading = false;
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    }
  }
};
</script>

<style scoped>
.admin-login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #d8caae;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #2e5626;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #E3E3E3;
  border-radius: 4px;
  box-sizing: border-box;
  height: 40px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #2e5626;
}

input {
  width: 100%;
  padding: 8px;
  border: 1px solid #E3E3E3;
  border-radius: 4px;
}

.password-input {
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

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #2e5626;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover:not(:disabled) {
  background-color: #4a7b2a;
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  color: #d9534f;
  text-align: center;
  margin-top: 10px;
}
</style>
