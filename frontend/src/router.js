import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import UserList from './components/UserList.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/users', component: UserList },
  { path: '/:pathMatch(.*)*', component: () => import('./components/NotFound.vue') }, // Route pour les pages non trouvées
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
