<template>
  <div>
    <h1>Connexion Parent</h1>
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Nom d'utilisateur" required />
      <input v-model="password" type="password" placeholder="Mot de passe" required />
      <button type="submit">Se connecter</button>
    </form>
  </div>
</template>

<script>
import api from '../../http-common';

export default {
  name: 'ParentLogin',
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await api.post('parent/login/', {
          json: {
            username: this.username,
            password: this.password,
          }
        }).json();
        localStorage.setItem('token', response.token);
        localStorage.setItem('userType', 'parent');
        this.$router.push('/parent-dashboard');
      } catch (error) {
        console.error('Erreur lors de la connexion:', error);
      }
    },
  },
};
</script>

<style scoped>
/* Styles inchangés */
</style>
