<template>
  <div class="admin-login">
    <h1>Connexion Administration</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Nom d'utilisateur</label>
        <input id="username" v-model="username" type="text" required>
      </div>
      <div class="form-group">
        <label for="password">Mot de passe</label>
        <div class="password-input">
          <input 
            id="password" 
            v-model="password" 
            :type="showPassword ? 'text' : 'password'" 
            required
          >
          <button 
            type="button" 
            @click="togglePasswordVisibility" 
            class="toggle-password"
          >
            {{ showPassword ? 'Cacher' : 'Afficher' }}
          </button>
        </div>
      </div>
      <button type="submit" class="submit-btn" :disabled="isLoading">
        {{ isLoading ? 'Connexion...' : 'Se connecter' }}
      </button>
    </form>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from '@/http-common';

export default {
  name: 'AdminLogin',
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
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },
    async login() {
      this.isLoading = true;
      this.errorMessage = '';
      try {
        const response = await api.post('api/token/', {
          json: {
            username: this.username,
            password: this.password,
          }
        }).json();

        if (response.access) {
          localStorage.setItem('token', response.access);
          localStorage.setItem('userType', 'admin');
          this.$router.push('/admin');
        } else {
          throw new Error('Token non reçu');
        }
      } catch (error) {
        console.error('Erreur lors de la connexion:', error);
        this.errorMessage = "Nom d'utilisateur ou mot de passe incorrect.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.admin-login {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  background-color: #FFFFFF;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #436F8A;
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  color: #333;
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
  background-color: #FFB347;
  color: white;
  border: none;
  padding: 8px 12px;
  cursor: pointer;
  border-radius: 0 4px 4px 0;
}

.submit-btn {
  width: 100%;
  padding: 10px;
  background-color: #436F8A;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.submit-btn:hover:not(:disabled) {
  background-color: #365870;
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
