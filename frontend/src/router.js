import { useAuthStore } from '@/stores/auth';
import MainView from '@/views/MainView.vue';
import Home from '@/components/common/Home.vue';
import NotFound from '@/components/common/NotFound.vue';
import Forbidden from '@/components/common/Forbidden.vue';

import { createRouter, createWebHistory } from 'vue-router';

const CreateAdmin = () => import('@/components/admin/CreateAdmin.vue');
const AdminLogin = () => import('@/components/admin/AdminLogin.vue');
const AdminDashboard = () => import('@/components/admin/AdminDashboard.vue');
const ParentsLogin = () => import('@/components/parents/ParentsLogin.vue');
const ParentsDashboard = () => import('@/components/parents/ParentsDashboard.vue');

const ROUTE_NAMES = {
  HOME: 'Home',
  ADMIN_LOGIN: 'AdminLogin',
  ADMIN_DASHBOARD: 'AdminDashboard',
  CREATE_ADMIN: 'CreateAdmin',
  ADD_ADMIN: 'AddAdmin',
  PARENTS_LOGIN: 'ParentsLogin',
  PARENTS_DASHBOARD: 'ParentsDashboard',
  NOT_FOUND: 'NotFound',
  FORBIDDEN: 'Forbidden'
};

const USER_TYPES = {
  SCHOOL_ADMIN: 'school_admin',
  DJANGO_ADMIN: 'django_admin',
  PARENT: 'parent'
};

const routes = [
  {
    path: '/',
    component: MainView,
    children: [
      { path: '', name: ROUTE_NAMES.HOME, component: Home },
      { path: 'parent-login', name: ROUTE_NAMES.PARENTS_LOGIN, component: ParentsLogin },
      {
        path: 'parent-dashboard',
        name: ROUTE_NAMES.PARENTS_DASHBOARD,
        component: ParentsDashboard,
        meta: { requiresAuth: true, userType: USER_TYPES.PARENT }
      },
      { path: 'admin/login', name: ROUTE_NAMES.ADMIN_LOGIN, component: AdminLogin },
      {
        path: 'create-admin',
        name: ROUTE_NAMES.CREATE_ADMIN,
        component: CreateAdmin,
        meta: { requiresAuth: false, onlyIfNoAdminExists: true }
      },
      {
        path: 'admin',
        name: ROUTE_NAMES.ADMIN_DASHBOARD,
        component: AdminDashboard,
        meta: { requiresAuth: true, userType: USER_TYPES.SCHOOL_ADMIN }
      },
      {
        path: 'add-admin',
        name: ROUTE_NAMES.ADD_ADMIN,
        component: CreateAdmin,
        meta: { requiresAuth: true, userType: USER_TYPES.ADMIN }
      },
      { path: 'forbidden', name: ROUTE_NAMES.FORBIDDEN, component: Forbidden },
      { path: ':pathMatch(.*)*', name: ROUTE_NAMES.NOT_FOUND, component: NotFound },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

let adminExistsCache = null;
let lastCheckTime = 0;
const CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

async function checkAdminExists() {
  const now = Date.now();
  if (adminExistsCache !== null && now - lastCheckTime < CACHE_DURATION) {
    return adminExistsCache;
  }

  try {
    const response = await fetch('http://localhost:8000/api/administrations/');
    if (!response.ok) {
      throw new Error('Erreur réseau lors de la vérification des administrateurs');
    }
    const admins = await response.json();
    adminExistsCache = admins.length > 0;
    lastCheckTime = now;
    return adminExistsCache;
  } catch (error) {
    console.error('Erreur lors de la vérification des administrateurs:', error);
    return false;
  }
}

checkAdminExists.invalidateCache = () => {
  adminExistsCache = null;
  lastCheckTime = 0;
};

function isAuthenticated(requiredType) {
  const authStore = useAuthStore();
  console.log('Checking authentication:', authStore.userInfo, authStore.userType, requiredType);
  return authStore.userInfo && (!requiredType || authStore.userType === requiredType);
}

router.beforeEach(async (to, from, next) => {
  try {
    const adminExists = await checkAdminExists();
    console.log('Admin exists:', adminExists);

    if (!adminExists && to.name !== ROUTE_NAMES.CREATE_ADMIN) {
      console.log('Redirecting to create admin');
      next({ name: ROUTE_NAMES.CREATE_ADMIN });
      return;
    }

    if (to.name === ROUTE_NAMES.CREATE_ADMIN && adminExists) {
      console.log('Admin exists, redirecting to admin login');
      next({ name: ROUTE_NAMES.ADMIN_LOGIN });
      return;
    }

    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!isAuthenticated(to.meta.userType)) {
        console.log('User not authenticated or wrong user type');
        next({ name: ROUTE_NAMES.ADMIN_LOGIN });
      } else {
        console.log('User authenticated, proceeding to route');
        next();
      }
    } else {
      console.log('No auth required, proceeding to route');
      next();
    }
  } catch (error) {
    console.error('Error during navigation:', error);
    next({ name: ROUTE_NAMES.FORBIDDEN });
  }
});

export { checkAdminExists };
export default router;
