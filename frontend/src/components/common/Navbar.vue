<template>
  <nav class="bg-[#0c2510] p-4 text-white flex justify-between items-center rounded-b-lg">
    <router-link to="/" class="text-lg font-bold no-underline text-[#ebe1d0] hover:text-gray-300">
      My Cantine Connect
    </router-link>
    <div class="space-x-4">
      <button @click="goToAdminLogin" 
              class="bg-[#2e5626] hover:bg-[#4a7b2a] text-[#ebe1d0] font-bold py-2 px-4 rounded-xlborder border-[#ebe1d0] focus:outline-none focus:ring-2 focus:ring-[#ebe1d0]"
              style="border-radius: 0.75rem;"
              >
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
      this.$router.push('/admin/login'); // Redirects to administrator login page
    },
  },
};
</script>

<style scoped>
/* Add specific styles if necessary */
</style>
