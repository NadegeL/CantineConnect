<template>
  <div class="forbidden">
    <h1>403 - Accès interdit</h1>
    <p>Vous n'avez pas la permission d'accéder à cette page.</p>
    <button @click="goBack" class="back-button">Retour</button>
  </div>
</template>

<script>
export default {
  name: 'Forbidden',
  methods: {
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.forbidden {
  text-align: center;
  margin-top: 50px;
  color: #436F8A;
  background-color: #FFFFFF;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.forbidden h1 {
  font-size: 2.5em;
  color: #436F8A;
  margin-bottom: 20px;
}

.forbidden p {
  font-size: 1.2em;
  color: #3A6351;
  margin-bottom: 30px;
}

.back-button {
  background-color: #FFB347;
  color: #FFFFFF;
  border: none;
  padding: 10px 20px;
  font-size: 1em;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.back-button:hover {
  background-color: #FF9914;
}
</style>
