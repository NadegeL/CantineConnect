<template>
  <div class="flex flex-col min-h-screen">
    <Navbar v-if="!$route.meta.hideNavbar" />
    <HeaderComponent v-if="!$route.meta.hideHeader" />
    <MainContent>
      <router-view></router-view>
    </MainContent>
    <FooterComponent v-if="!$route.meta.hideFooter" />
  </div>
</template>

<script>
import Navbar from '@/components/common/Navbar.vue';
import HeaderComponent from '@/components/common/HeaderComponent.vue';
import FooterComponent from '@/components/common/FooterComponent.vue';
import MainContent from '@/components/common/MainContent.vue';

export default {
  name: 'MainView',
  components: {
    Navbar,
    HeaderComponent,
    FooterComponent,
    MainContent,
  },
};
</script>

<style scoped>
/* Add specific styles if necessary */
</style>
