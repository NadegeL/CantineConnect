import { defineStore } from 'pinia';

import ky from 'ky';

const API_BASE_URL = 'http://localhost:8000/api';
const STORAGE_KEYS = {
  TOKEN: 'token',
  REFRESH_TOKEN: 'refreshToken',
  USER_TYPE: 'userType',
  USER_INFO: 'userInfo'
};

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem(STORAGE_KEYS.TOKEN) || null,
    refreshToken: localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN) || null,
    userType: localStorage.getItem(STORAGE_KEYS.USER_TYPE) || null,
    userInfo: JSON.parse(localStorage.getItem(STORAGE_KEYS.USER_INFO)) || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isParent: (state) => state.userType === USER_TYPES.PARENT,
    isSchoolAdmin: (state) => state.userType === USER_TYPES.SCHOOL_ADMIN,
    hasVueAccess: (state) => [USER_TYPES.PARENT, USER_TYPES.SCHOOL_ADMIN].includes(state.userType), // Accès uniquement aux 'parent' et 'school_admin'
  },
  actions: {
    async login(email, password) {
      try {
        const response = await ky.post(`${API_BASE_URL}/token/`, {
          json: { email, password },
        }).json();
        this.setAuthData(response);
        console.log('Login successful, user info:', this.userInfo);
      } catch (error) {
        console.error('Login failed:', error.message);
        throw new Error('Échec de la connexion. Veuillez vérifier vos identifiants.');
      }
    },
    async refreshToken() {
      if (!this.refreshToken) {
        throw new Error('Aucun token de rafraîchissement disponible');
      }
      try {
        const response = await ky.post(`${API_BASE_URL}/token/refresh/`, {
          json: { refresh: this.refreshToken },
        }).json();
        this.token = response.access;
        sessionStorage.setItem(STORAGE_KEYS.TOKEN, this.token);
        return this.token;
      } catch (error) {
        console.error('Erreur lors du rafraîchissement du token:', error.message);
        this.logout();
        throw new Error('La session a expiré. Veuillez vous reconnecter.');
      }
    },
    logout() {
      this.clearAuthData();
    },
    setAuthData(data) {
      this.token = data.access;
      this.refreshToken = data.refresh;
      this.userType = data.user_type;
      this.userInfo = {
        email: data.email,
        first_name: data.first_name,
        last_name: data.last_name,
      };
      sessionStorage.setItem(STORAGE_KEYS.TOKEN, this.token);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, this.refreshToken);
      localStorage.setItem(STORAGE_KEYS.USER_TYPE, this.userType);
      localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(this.userInfo));
    },
    clearAuthData() {
      this.token = null;
      this.refreshToken = null;
      this.userType = null;
      this.userInfo = null;
      sessionStorage.removeItem(STORAGE_KEYS.TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER_TYPE);
      localStorage.removeItem(STORAGE_KEYS.USER_INFO);
    },
    async checkAuth() {
      if (this.token) {
        try {
          await this.refreshToken();
        } catch (error) {
          this.clearAuthData();
        }
      }
    }
  },
});
