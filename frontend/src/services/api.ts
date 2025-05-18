import axios from 'axios';

export const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

// Add a request interceptor to include the token in all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  console.log('Making request with token:', token);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle token errors
api.interceptors.response.use(
  (response) => {
    console.log('✅ API response:', response.status, response.data);
    return response;
  },
  async (error) => {
    // Log the full error details with a more visible format
    console.error('%c🔴 API ERROR', 'color: red; font-size: 16px; font-weight: bold;');
    console.error('%cError Details:', 'color: red; font-weight: bold;', {
      status: error.response?.status,
      data: error.response?.data,
      headers: error.response?.headers,
      config: error.config,
      message: error.message
    });
    
    // Check if we got a new token in the response
    const newToken = error.response?.headers?.['x-new-token'];
    if (error.response?.status === 401 && newToken) {
      console.log('%c🟢 Received new token, updating...', 'color: green; font-weight: bold;');
      localStorage.setItem('token', newToken);
      
      // Retry the original request with the new token
      const config = error.config;
      config.headers.Authorization = `Bearer ${newToken}`;
      return api(config);
    }
    
    if (error.response?.status === 401) {
      console.log('%c🔴 Token expired or invalid, redirecting to login...', 'color: red; font-weight: bold;');
      // Clear invalid token
      localStorage.removeItem('token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const auth = {
  API_URL,
  login: () => {
    window.location.href = `${API_URL}/login`;
  },
  logout: async () => {
    try {
      await api.post('/logout');
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('spotify_code');
      window.location.href = '/';
    }
  },
  getMe: async () => {
    console.log('Calling getMe endpoint');
    const response = await api.get('/me');
    console.log('getMe response:', response.data);
    return response.data;
  },
  handleCallback: async (code: string) => {
    try {
      const response = await api.post('/callback', { code });
      return response.data;
    } catch (error) {
      console.error('Error handling callback:', error);
      throw error;
    }
  }
};

export const spotify = {
  getTopTracks: async (timeRange: string = 'medium_term') => {
    const response = await api.get(`/spotify/top-tracks?time_range=${timeRange}`);
    return response.data;
  },
  getTopArtists: async (timeRange: string = 'medium_term') => {
    const response = await api.get(`/spotify/top-artists?time_range=${timeRange}`);
    return response.data;
  },
  getRecentlyPlayed: async () => {
    const response = await api.get('/spotify/recently-played');
    return response.data;
  },
}; 