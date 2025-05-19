import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { auth } from "../services/api";

const API_URL = import.meta.env.VITE_API_URL;

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
  document.cookie.split(";").forEach((cookie) => {
    document.cookie = cookie
      .replace(/^ +/, "")
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
        const storedToken = localStorage.getItem("token");
        if (!storedToken) {
          resetState();
          setLoading(false);
          return;
        }

        await auth.getMe();
        setToken(storedToken);
        setError(null);
      } catch {
        resetState();
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    // Check for token or error in URL
    const tokenFromUrl = searchParams.get("token");
    const errorFromUrl = searchParams.get("error");

    if (tokenFromUrl) {
      // Reset everything before setting new token
      resetState();

      // Store the JWT token
      localStorage.setItem("token", tokenFromUrl);
      setToken(tokenFromUrl);
      setError(null);
      // Remove token from URL
      window.history.replaceState({}, document.title, window.location.pathname);
    } else if (errorFromUrl) {
      resetState();
      setError(errorFromUrl);
      // Remove error from URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, [searchParams]);

  const logout = async () => {
    try {
      // First, log out from app
      await fetch(`${API_URL}/logout`, {
        method: "POST",
        credentials: "include",
      });

      // Clear all local storage
      localStorage.clear();
      sessionStorage.clear();
      setToken(null);
      setError(null);

      // Redirect to home page
      window.location.href = "/";
    } catch {
      setError("Failed to logout");
    }
  };

  return { token, error, loading, logout };
}
