import { ACCESS_TOKEN_KEY, API_BASE_URL, TOKEN_EVENT } from './config';

let accessToken: string | null =
  typeof window === 'undefined'
    ? null
    : window.localStorage.getItem(ACCESS_TOKEN_KEY);

const listeners = new Set<(token: string | null) => void>();

export function getAccessToken() {
  return accessToken;
}

export function setAccessToken(token: string | null) {
  accessToken = token;
  if (typeof window !== 'undefined') {
    if (token) {
      window.localStorage.setItem(ACCESS_TOKEN_KEY, token);
    } else {
      window.localStorage.removeItem(ACCESS_TOKEN_KEY);
    }
    window.dispatchEvent(new CustomEvent(TOKEN_EVENT, { detail: token }));
  }
  listeners.forEach((listener) => listener(token));
}

export function subscribeToTokenUpdates(listener: (token: string | null) => void) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

if (typeof window !== 'undefined') {
  window.addEventListener(TOKEN_EVENT, ((event: Event) => {
    const detail = (event as CustomEvent<string | null>).detail ?? null;
    accessToken = detail;
    listeners.forEach((listener) => listener(detail));
  }) as EventListener);
}

export function extractAccessToken(response: {
  ['access token']?: string;
  ['access token:']?: string;
}): string | null {
  return response['access token'] ?? response['access token:'] ?? null;
}

export async function refreshAccessToken(): Promise<string | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      return null;
    }

    const data = (await response.json()) as { 'access token'?: string };
    const newToken = data['access token'] ?? null;
    setAccessToken(newToken);
    return newToken;
  } catch {
    return null;
  }
}
