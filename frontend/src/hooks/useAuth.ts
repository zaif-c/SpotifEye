import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { auth } from '../services/api';

const API_URL = 'http://localhost:8000';

interface TokenData {
  access_token: string;
  token_type: string;
  expires_in: number;
  scope: string;
  expires_at: number;
  refresh_token: string;
}

interface AuthState {
  token: string | null;
  error: string | null;
  loading: boolean;
  logout: () => Promise<void>;
}

// Clear all browser storage
const clearAllStorage = () => {
  // Clear localStorage
  localStorage.clear();
  // Clear sessionStorage
  sessionStorage.clear();
  // Clear all cookies
  document.cookie.split(';').forEach(cookie => {
    document.cookie = cookie
      .replace(/^ +/, '')
      .replace(/=.*/, `=;expires=${new Date(0).toUTCString()};path=/`);
  });
};

export function useAuth(): AuthState {
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Reset all state and storage
  const resetState = () => {
    clearAllStorage();
    setToken(null);
    setError(null);
  };

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const storedToken = localStorage.getItem('token');
        if (!storedToken) {
          resetState();
          setLoading(false);
          return;
        }

        await auth.getMe();
        setToken(storedToken);
        setError(null);
      } catch (err) {
        console.error('Auth check failed:', err);
        resetState();
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    // Check for token or error in URL
    const tokenFromUrl = searchParams.get('token');
    const errorFromUrl = searchParams.get('error');

    console.log('🔍 URL params:', { tokenFromUrl, errorFromUrl });

    if (tokenFromUrl) {
      console.log('✅ Setting token from URL:', tokenFromUrl);
      // Reset everything before setting new token
      resetState();
      
      // Store the JWT token
      localStorage.setItem('token', tokenFromUrl);
      setToken(tokenFromUrl);
      setError(null);
      // Remove token from URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (errorFromUrl) {
      console.error('🔴 Error from URL:', errorFromUrl);
      resetState();
      setError(errorFromUrl);
      // Remove error from URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [searchParams]);

  const logout = async () => {
    try {
      console.log('Starting logout process...');
      // First, log out from our app
      console.log('Calling backend logout endpoint...');
      await fetch(`${API_URL}/logout`, {
        method: 'POST',
        credentials: 'include',
      });
      
      console.log('Backend logout successful, clearing storage...');
      // Clear all local storage
      localStorage.clear();
      sessionStorage.clear();
      setToken(null);
      setError(null);

      // Redirect to home page
      window.location.href = '/';
    } catch (err) {
      console.error('Logout error:', err);
      setError('Failed to logout');
    }
  };

  return { token, error, loading, logout };
} 