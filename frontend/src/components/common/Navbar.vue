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
