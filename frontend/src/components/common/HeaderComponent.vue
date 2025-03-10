<template>
  <header style="background-color: #e8f5e9;" class="p-4 flex flex-col items-center">
    <!-- Logo -->
    <img src="@/assets/Logo.png" alt="Cantine Connect" class="h-24 mb-2" />

    <!-- Navigation -->
    <nav class="mt-4 w-full max-w-2xl">
      <ul class="flex justify-center space-x-6 text-green-800 font-medium">
        <li class="hover:text-green-600 transition-colors cursor-pointer px-3 py-1">Accueil</li>
        <li class="hover:text-green-600 transition-colors cursor-pointer px-3 py-1">Élèves</li>
        <li class="hover:text-green-600 transition-colors cursor-pointer px-3 py-1">Repas</li>
        <li class="hover:text-green-600 transition-colors cursor-pointer px-3 py-1">Facturation</li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'HeaderComponent',
};
</script>