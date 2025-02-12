<template>
  <div>
    <h1>Liste des utilisateurs</h1>
    <ul>
      <li v-for="user in users" :key="user.id">{{ user.name }}</li>
    </ul>
  </div>
</template>

<script>
import api from '../http-common';

export default {
  name: 'UserList',
  data() {
    return {
      users: [],
    };
  },
  methods: {
    async retrieveUsers() {
      try {
        const response = await api.get('users/').json();
        this.users = response;
      } catch (error) {
        console.error('Erreur lors de la récupération des utilisateurs:', error);
      }
    },
  },
  mounted() {
    this.retrieveUsers();
  },
};
</script>
