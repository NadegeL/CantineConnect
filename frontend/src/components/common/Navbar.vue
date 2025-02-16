<template>
  <nav class="bg-gray-800 p-4 text-white flex justify-between items-center">
    <router-link to="/" class="text-lg font-bold no-underline text-white hover:text-gray-300">
      Mon Application
    </router-link>
    <div class="space-x-4">
      <button @click="goToAdminLogin" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
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
      this.$router.push('/admin/login'); // Redirige vers la page de connexion administrateur
    },
  },
};
</script>

<style scoped>
/* Ajoutez des styles spécifiques si nécessaire */
</style>
