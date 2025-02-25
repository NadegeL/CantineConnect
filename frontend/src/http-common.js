import ky from 'ky';

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

async function refreshToken() {
  const refreshToken = localStorage.getItem('refreshToken');
  if (!refreshToken) {
    throw new Error('No refresh token available');
  }

  try {
    const response = await ky.post('http://localhost:8000/api/token/refresh/', {
      json: { refresh: refreshToken },
    }).json();

    localStorage.setItem('token', response.access);
    return response.access;
  } catch (error) {
    console.error('Error refreshing token:', error);
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    throw error;
  }
}

const api = ky.extend({
  prefixUrl: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
  hooks: {
    beforeRequest: [
      request => {
        const csrfToken = getCookie('csrftoken');
        if (csrfToken) {
          request.headers.set('X-CSRFToken', csrfToken);
        }

        const token = localStorage.getItem('token');
        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`);
        }
      }
    ],
    afterResponse: [
      async (request, options, response) => {
        if (response.status === 401) {
          try {
            const newToken = await refreshToken();
            request.headers.set('Authorization', `Bearer ${newToken}`);
            return ky(request);
          } catch (error) {
            console.error('Token refresh failed:', error);
            // Rediriger vers la page de connexion ou gérer l'erreur
            window.location.href = '/login';
          }
        }
        return response;
      }
    ]
  },
  retry: 0,
});

export default api;
