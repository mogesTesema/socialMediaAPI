import type {
  AuthResponse,
  Comment,
  Post,
  PostSorting,
  PostWithComments,
} from './types';

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ||
  'http://localhost:8000';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: Record<string, unknown>;
  token?: string | null;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, token } = options;
  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers: {
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
    credentials: 'include',
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const message = errorBody?.detail || response.statusText;
    throw new Error(message);
  }

  return response.json();
}

export const api = {
  register: (email: string, password: string) =>
    request<AuthResponse>('/register', {
      method: 'POST',
      body: { email, password },
    }),
  login: (email: string, password: string) =>
    request<AuthResponse>('/login', {
      method: 'POST',
      body: { email, password },
    }),
  requestPasswordReset: (email: string) =>
    request<{ status: string }>('/password/forgot', {
      method: 'POST',
      body: { email },
    }),
  resetPassword: (token: string, newPassword: string) =>
    request<{ status: string }>('/password/reset', {
      method: 'POST',
      body: { token, new_password: newPassword },
    }),
  getPosts: (sorting: PostSorting) =>
    request<Post[]>(`/posts?sorting=${sorting}`),
  createPost: (token: string, body: string) =>
    request<Post>('/post', {
      method: 'POST',
      body: { body },
      token,
    }),
  likePost: (token: string, postId: number) =>
    request<{ id: number; post_id: number; user_id: number }>('/like', {
      method: 'POST',
      body: { post_id: postId },
      token,
    }),
  getPostComments: (postId: number) =>
    request<PostWithComments>(`/post/${postId}/comments`),
  addComment: (token: string, postId: number, body: string) =>
    request<Comment>('/comment', {
      method: 'POST',
      body: { post_id: postId, body },
      token,
    }),
  predictFood: async (file: File) => {
    const form = new FormData();
    form.append('file', file);

    const response = await fetch(`${API_BASE_URL}/food-vision/predict`, {
      method: 'POST',
      body: form,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const message = errorBody?.detail || response.statusText;
      throw new Error(message);
    }

    return response.json() as Promise<{ filename: string; predictions: { label: string; score_percent: number }[] }>;
  },
};
