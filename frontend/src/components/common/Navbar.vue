<template>
  <nav class="navbar">
    <router-link to="/" class="navbar-brand">
      Mon Application
    </router-link>
    <div>
      <button @click="goToAdminLogin" class="btn-primary">
        Connexion Administrateur
      </button>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar',
  methods: {
    goToAdminLogin() {
      this.$router.push('/admin/login');
    },
  },
};
</script>

<style scoped>
.navbar {
  background-color: #436F8A;
  color: #FFFFFF;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 1.25rem;
  font-weight: bold;
  text-decoration: none;
  color: #FFFFFF;
}

.navbar-brand:hover {
  color: #E3E3E3;
}

.btn-primary {
  background-color: #FFB347;
  color: #FFFFFF;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary:hover {
  background-color: #FFA500;
}
</style>
