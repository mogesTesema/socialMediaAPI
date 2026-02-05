import { createContext, ReactNode, useContext, useMemo, useState } from 'react';

interface AuthContextValue {
  accessToken: string | null;
  setAccessToken: (token: string | null) => void;
  clearSession: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

const ACCESS_TOKEN_KEY = 'fooddeals_access_token';

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
    }
  };

  const clearSession = () => setAccessToken(null);

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
