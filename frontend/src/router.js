import MainView from '@/views/MainView.vue';
import Home from '@/components/common/Home.vue';
import CreateAdmin from '@/components/admin/CreateAdmin.vue';
import AdminLogin from '@/components/admin/AdminLogin.vue';
import AdminDashboard from '@/components/admin/AdminDashboard.vue';
import ParentsLogin from '@/components/parents/ParentsLogin.vue';
import ParentsDashboard from '@/components/parents/ParentsDashboard.vue';
import NotFound from '@/components/common/NotFound.vue';

import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    component: MainView,
    children: [
      { path: '', name: 'Home', component: Home },
      { path: 'parent-login', name: 'ParentsLogin', component: ParentsLogin },
      { 
        path: 'parent-dashboard', 
        name: 'ParentsDashboard',
        component: ParentsDashboard, 
        meta: { requiresAuth: true, userType: 'parent' }
      },
      { path: 'admin/login', name: 'AdminLogin', component: AdminLogin },
      { 
        path: 'create-admin', 
        name: 'CreateAdmin', 
        component: CreateAdmin,
        meta: { requiresAuth: false, onlyIfNoAdminExists: true }
      },
      { 
        path: 'admin', 
        name: 'AdminDashboard',
        component: AdminDashboard, 
        meta: { requiresAuth: true, userType: 'admin' }
      },
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Cache pour éviter les requêtes répétées
let adminExistsCache = null;

// Vérifie si un administrateur existe dans la base de données
async function checkAdminExists() {
  if (adminExistsCache !== null) {
    return adminExistsCache;
  }
  try {
    const response = await fetch('http://localhost:8000/api/administrations/');
    const admins = await response.json();
    adminExistsCache = admins.length > 0;
    return adminExistsCache;
  } catch (error) {
    console.error('Erreur lors de la vérification des administrateurs:', error);
    return false;
  }
}

// Vérifie si l'utilisateur est authentifié et a le bon type
function isAuthenticated(requiredType) {
  const token = localStorage.getItem('token');
  const userType = localStorage.getItem('userType');
  return token && (!requiredType || userType === requiredType);
}

// Guard de navigation
router.beforeEach(async (to, from, next) => {
  const adminExists = await checkAdminExists();

  // Si aucun administrateur n'existe, rediriger automatiquement vers /create-admin
  if (!adminExists && to.name !== 'CreateAdmin') {
    next({ name: 'CreateAdmin' });
    return;
  }

  // Bloque l'accès à /create-admin si un administrateur existe déjà
  if (to.name === 'CreateAdmin' && adminExists) {
    next({ name: 'AdminLogin' });
    return;
  }

  // Vérifie les routes nécessitant une authentification
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const requiredType = to.meta.userType;
    if (!isAuthenticated(requiredType)) {
      next({ name: requiredType === 'admin' ? 'AdminLogin' : 'ParentsLogin' });
      return;
    }
  }

  // Autoriser la navigation si aucune condition n'est bloquante
  next();
});

export default router;
