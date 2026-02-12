import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';
import { ACCESS_TOKEN_KEY, TOKEN_EVENT } from '../../lib/config';
import type { UserProfile } from '../../lib/types';
import { api } from '../../lib/api';

interface AuthContextValue {
  accessToken: string | null;
  user: UserProfile | null;
  setAccessToken: (token: string | null) => void;
  clearSession: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [accessToken, setAccessTokenState] = useState<string | null>(() =>
    typeof window === 'undefined'
      ? null
      : window.localStorage.getItem(ACCESS_TOKEN_KEY),
  );
  const [user, setUser] = useState<UserProfile | null>(null);

  const fetchUser = async (token: string) => {
    try {
      const userData = await api.getProfile(token);
      setUser(userData);
    } catch (e) {
      console.error(e); // Silent fail on profile fetch
    }
  };

  const setAccessToken = (token: string | null) => {
    setAccessTokenState(token);
    if (token) {
       fetchUser(token);
    } else {
       setUser(null);
    }
    
    if (typeof window !== 'undefined') {
      if (token) {
        window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
      } else {
        window.localStorage.removeItem(ACCESS_TOKEN_KEY);
      }
      window.dispatchEvent(new CustomEvent(TOKEN_EVENT, { detail: token }));
    }
  };

  const clearSession = () => setAccessToken(null);

  useEffect(() => {
    const handler = (event: Event) => {
      const detail = (event as CustomEvent<string | null>).detail ?? null;
      setAccessTokenState(detail);
      if (detail) {
         fetchUser(detail);
      } else {
         setUser(null);
      }
    };
    window.addEventListener(TOKEN_EVENT, handler as EventListener);
    
    // Initial fetch if token exists
    if (accessToken) {
       fetchUser(accessToken);
    }

    return () => window.removeEventListener(TOKEN_EVENT, handler as EventListener);
  }, []);

  const value = useMemo(
    () => ({ accessToken, user, setAccessToken, clearSession }),
    [accessToken, user],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
