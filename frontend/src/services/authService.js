import { useAuthStore } from '@/stores/auth';

export const logout = async () => {
  const authStore = useAuthStore();
  try {
    console.log('Déconnexion...');
    await authStore.logout();
  } catch (error) {
    console.error('Erreur lors de la déconnexion:', error);
    throw error;
  }
};
