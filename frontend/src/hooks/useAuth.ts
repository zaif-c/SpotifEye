import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { auth } from '../services/api';

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

export function useAuth(): AuthState {
  const [searchParams] = useSearchParams();
  const [token, setToken] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const storedToken = localStorage.getItem('token');
        if (!storedToken) {
          setToken(null);
          setError(null);
          setLoading(false);
          return;
        }

        await auth.getMe();
        setToken(storedToken);
        setError(null);
      } catch (err) {
        console.error('Auth check failed:', err);
        setToken(null);
        setError('Authentication failed. Please try logging in again.');
        localStorage.removeItem('token');
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
      // Store the JWT token directly
      setToken(tokenFromUrl);
      localStorage.setItem('token', tokenFromUrl);
      setError(null);
      // Remove token from URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (errorFromUrl) {
      console.error('🔴 Error from URL:', errorFromUrl);
      setError(errorFromUrl);
      localStorage.removeItem('token');
      setToken(null);
      // Remove error from URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [searchParams]);

  const logout = async () => {
    try {
      await auth.logout();
      setToken(null);
      setError(null);
    } catch (err) {
      console.error('Logout failed:', err);
      setError('Failed to logout. Please try again.');
    }
  };

  return { token, error, loading, logout };
} 