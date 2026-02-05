import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react';
import { ACCESS_TOKEN_KEY, TOKEN_EVENT } from '../../lib/config';

interface AuthContextValue {
  accessToken: string | null;
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

  const setAccessToken = (token: string | null) => {
    setAccessTokenState(token);
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
    };
    window.addEventListener(TOKEN_EVENT, handler as EventListener);
    return () => window.removeEventListener(TOKEN_EVENT, handler as EventListener);
  }, []);

  const value = useMemo(
    () => ({ accessToken, setAccessToken, clearSession }),
    [accessToken],
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
