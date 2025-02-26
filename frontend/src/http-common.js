import { useAuthStore } from '@/stores/auth';

import ky from 'ky';

const api = ky.create({
  prefixUrl: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  credentials: 'include',
  hooks: {
    beforeRequest: [
      request => {
        const authStore = useAuthStore();
        const csrfToken = getCookie('csrftoken');
        if (csrfToken) {
          console.log('CSRF Token added to headers:', csrfToken);
          request.headers.set('X-CSRFToken', csrfToken);
        }
        if (!request.url.includes('/api/school-zones/')) {
          if (authStore.token) {
            console.log('Authorization Token added to headers:', authStore.token);
            request.headers.set('Authorization', `Bearer ${authStore.token}`);
          }
        }
      }
    ],
    afterResponse: [
      async (request, options, response) => {
        if (response.status === 401) {
          const authStore = useAuthStore();
          try {
            console.log('Token expired, attempting to refresh...');
            const newToken = await authStore.refreshToken();
            request.headers.set('Authorization', `Bearer ${newToken}`);
            return ky(request);
          } catch (error) {
            console.error('Token refresh failed:', error);
            authStore.logout();
            // Vous pouvez gérer la redirection ici si nécessaire
            // window.location.href = '/login';
          }
        }
      }
    ]
  },
  retry: 0,
});

export default api;

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
