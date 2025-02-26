<template>
  <main class="main-content">
    <slot></slot>
  </main>
</template>

<script>
export default {
  name: 'MainContent',
};
</script>

<style scoped>
.main-content {
  flex: 1;
  padding: 1rem;
  background-color: #E3E3E3;
}
</style>
