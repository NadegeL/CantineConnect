<template>
  <div class="not-found">
    <h1>404 - Page non trouvée</h1>
    <p>La page que vous cherchez n'existe pas.</p>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
};
</script>

<style scoped>
.not-found {
  text-align: center;
  margin-top: 50px;
  color: #ff6f61;
  background-color: #fff3e0;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.not-found h1 {
  font-size: 2.5em;
  color: #ff5722;
}

.not-found p {
  font-size: 1.2em;
  color: #ff8a65;
}
</style>
