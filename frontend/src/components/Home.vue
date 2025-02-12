<!-- src/components/Home.vue -->
<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <header class="bg-blue-600 text-white p-4 rounded-md shadow-md">
      <h1 class="text-2xl font-semibold">Bienvenue sur CantineConnect</h1>
    </header>

    <!-- Main Content -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Card 1 -->
      <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-xl font-semibold mb-2">Réservations de repas</h2>
        <p class="text-gray-700 mb-4">Gérez les réservations de repas pour vos enfants à la cantine.</p>
        <button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">Réserver maintenant</button>
      </div>

      <!-- Card 2 -->
      <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-xl font-semibold mb-2">Gestion des absences</h2>
        <p class="text-gray-700 mb-4">Suivez les absences des élèves et justifiez-les facilement.</p>
        <button class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700">Gérer les absences</button>
      </div>

      <!-- Card 3 -->
      <div class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-xl font-semibold mb-2">Allergies et restrictions</h2>
        <p class="text-gray-700 mb-4">Ajoutez et gérez les allergies alimentaires des enfants pour éviter les risques.</p>
        <button class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700">Gérer les allergies</button>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white p-4 rounded-md mt-8 text-center">
      <p>© 2025 CantineConnect | Tous droits réservés</p>
    </footer>
  </div>
</template>

<script setup>
// Ce script est vide pour l'exemple, mais tu peux y ajouter de la logique JavaScript si nécessaire.
</script>

<style scoped>
/* Style global pour les éléments */
h1,
h2 {
  font-family: 'Arial', sans-serif;
}
</style>
