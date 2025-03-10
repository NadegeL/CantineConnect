<template>
  <div class="not-found-page" :style="{ backgroundImage: `url(${logoPath})` }">
    <div class="overlay" :class="{ 'fade-in': backgroundLoaded }"></div>

    <div class="content-container">
      <h1 class="text-center text-green-800 text-5xl font-bold mb-4">404</h1>
      <h2 class="text-center text-green-800 text-3xl font-semibold mb-8">Page non trouvée</h2>

      <div class="bg-white bg-opacity-80 max-w-lg mx-auto rounded-lg shadow-md p-8 text-center">
        <p class="text-lg text-gray-700 mb-6">
          La page que vous recherchez n'existe pas ou a été déplacée.
        </p>

        <div class="flex justify-center gap-4">
          <button @click="goBack"
            class="bg-amber-500 hover:bg-amber-600 text-white py-2 px-4 rounded-md transition-colors">
            Retour
          </button>
          <button @click="goHome"
            class="bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md transition-colors">
            Accueil
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import logoImage from '@/assets/Logo.png'

export default {
  name: 'NotFound',
  data() {
    return {
      logoPath: logoImage,
      backgroundLoaded: false
    }
  },
  mounted() {
    this.hideNavbar();
    this.loadBackgroundImage();
  },
  beforeUnmount() {
    this.showNavbar();
  },
  methods: {
    loadBackgroundImage() {
      const img = new Image();
      img.src = this.logoPath;
      img.onload = () => {
        this.backgroundLoaded = true;
      };
    },
    hideNavbar() {
      const navbar = document.querySelector('.navbar');
      if (navbar) {
        navbar.style.display = 'none';
      }
    },
    showNavbar() {
      const navbar = document.querySelector('.navbar');
      if (navbar) {
        navbar.style.display = 'block';
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    goHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
.not-found-page {
  min-height: 100vh;
  width: 100%;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(232, 245, 233, 0.8);
  opacity: 0;
  transition: opacity 1.5s ease;
}

.overlay.fade-in {
  opacity: 1;
}

.content-container {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 800px;
}
</style>