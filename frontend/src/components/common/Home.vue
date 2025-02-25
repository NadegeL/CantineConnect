<template>
  <div class="home">
    <h1>Bienvenue sur CantineConnect</h1>
    <p>Veuillez vous connecter pour accéder à votre espace.</p>
    <div class="button-container">
      <button @click="goToParentsLogin" class="btn-parents">Connexion Parents</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    goToParentsLogin() {
      this.$router.push('/parent-login');
    },
    goToAdminLogin() {
      this.$router.push('/admin/login');
    },
  },
};
</script>

<style scoped>
.home {
  text-align: center;
  padding: 50px;
  background-color: #E3E3E3;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

h1 {
  color: #436F8A;
  margin-bottom: 20px;
}

p {
  color: #333;
  margin-bottom: 30px;
}

.button-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

button {
  padding: 12px 24px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.btn-parents {
  background-color: #FFB347;
  color: white;
}

.btn-admin {
  background-color: #436F8A;
  color: white;
}

button:hover {
  opacity: 0.9;
}
</style>
