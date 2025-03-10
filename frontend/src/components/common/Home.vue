<template>
  <div class="home-page" :style="{ backgroundImage: `url(${logoPath})` }">
    <div class="overlay" :class="{ 'fade-in': backgroundLoaded }"></div>
    
    <div class="content">
      <transition-group 
        name="word-animation" 
        tag="h1" 
        class="welcome-title"
      >
        <span key="welcome1" class="word">Bienvenue</span>
        <span key="welcome2" class="word">sur</span>
        <span key="welcome3" class="word">Cantine</span>
        <span key="welcome4" class="word">Connect</span>
      </transition-group>

      <div class="container-btns">
        <button @click="goToParentsLogin" class="btn-parents">Connexion Parents</button>
        <button @click="goToAdminLogin" class="btn-admin">Connexion Admin</button>
      </div>
    </div>
  </div>
</template>

<script>
import logoImage from '@/assets/Logo.png'

export default {
  name: 'HomePage',
  data() {
    return {
      logoPath: logoImage,
      backgroundLoaded: false
    }
  },
  mounted() {
    this.loadBackgroundImage()
    this.animateWelcomeText()
  },
  methods: {
    loadBackgroundImage() {
      const img = new Image()
      img.src = this.logoPath
      img.onload = () => {
        this.backgroundLoaded = true
      }
    },
    animateWelcomeText() {
      const words = document.querySelectorAll('.word')
      words.forEach((word, index) => {
        word.style.opacity = '0'
        word.style.transform = 'translateY(50px)'

        setTimeout(() => {
          word.style.transition = 'all 0.8s ease'
          word.style.opacity = '1'
          word.style.transform = 'translateY(0)'
        }, (index + 1) * 300)
      })
    },
    goToParentsLogin() {
      this.$router.push('/parent-login')
    },
    goToAdminLogin() {
      this.$router.push('/admin/login')
    }
  }
}
</script>

<style scoped>
.home-page {
  height: 100vh;
  width: 100vw;
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(232, 245, 233, 0.8); /* Couleur de fond vert clair semi-transparente */
  opacity: 0;
  transition: opacity 1.5s ease;
}

.overlay.fade-in {
  opacity: 1;
}

.content {
  text-align: center;
  z-index: 10;
  position: relative;
}

.welcome-title {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.welcome-title span {
  color: #2e5626;
  font-size: 3rem;
  opacity: 0;
}

.container-btns {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn-parents, .btn-admin {
  padding: 0.8rem 1.5rem;
  background-color: #2e5626;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-parents:hover, .btn-admin:hover {
  background-color: #4a7b2a;
}

/* Animations de transition */
.word-animation-enter-active,
.word-animation-leave-active {
  transition: all 0.5s;
}

.word-animation-enter,
.word-animation-leave-to {
  opacity: 0;
  transform: translateY(30px);
}
</style>