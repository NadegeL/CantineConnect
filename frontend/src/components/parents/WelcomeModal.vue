<template>
  <div class="modal">
    <div class="modal-content">
      <h2>Bienvenue sur notre plateforme !</h2>
      <p>Merci de rejoindre notre système. Avant de continuer, veuillez compléter votre profil.</p>
      <button @click="$emit('close')">Suivant</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WelcomeModal',
  emits: ['close']
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 5px;
  text-align: center;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
</style>
