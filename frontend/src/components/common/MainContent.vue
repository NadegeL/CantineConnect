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
  background-color: #e8f5e9;
}
</style>
