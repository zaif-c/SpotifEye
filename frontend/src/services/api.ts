import axios from "axios";

export const API_URL = "http://127.0.0.1:8000";

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

// Add a request interceptor to include the token in all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Add a response interceptor to handle token errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    // Check if new token received in the response
    const newToken = error.response?.headers?.["x-new-token"];
    if (error.response?.status === 401 && newToken) {
      localStorage.setItem("token", newToken);

      // Retry the original request with the new token
      const config = error.config;
      config.headers.Authorization = `Bearer ${newToken}`;
      return api(config);
    }

    if (error.response?.status === 401) {
      // Clear invalid token
      localStorage.removeItem("token");
      window.location.href = "/";
    }
    return Promise.reject(error);
  },
);

export const auth = {
  API_URL,
  login: () => {
    window.open(`${API_URL}/login`, '_self');
  },
  logout: async () => {
    await api.post("/logout");
    localStorage.removeItem("token");
    localStorage.removeItem("spotify_code");
    window.location.href = "/";
  },
  getMe: async () => {
    const response = await api.get("/me");
    return response.data;
  },
  handleCallback: async (code: string) => {
    const response = await api.post("/callback", { code });
    return response.data;
  },
};

export const spotify = {
  getTopTracks: async (timeRange: string = "medium_term", limit: number = 50) => {
    const response = await api.get(
      `/spotify/top-tracks?time_range=${timeRange}&limit=${limit}`,
    );
    return response.data;
  },
  getTopArtists: async (timeRange: string = "medium_term", limit: number = 50) => {
    const response = await api.get(
      `/spotify/top-artists?time_range=${timeRange}&limit=${limit}`,
    );
    return response.data;
  },
  getRecentlyPlayed: async () => {
    const response = await api.get("/spotify/recently-played");
    return response.data;
  },
};
