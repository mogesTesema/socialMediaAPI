export const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ||
  'http://localhost:8000';

export const ACCESS_TOKEN_KEY = 'fooddeals_access_token';
export const TOKEN_EVENT = 'fooddeals_token_updated';
