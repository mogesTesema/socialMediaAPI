import type {
  AuthResponse,
  Comment,
  Post,
  PostSorting,
  PostWithComments,
} from './types';
import { API_BASE_URL } from './config';
import { getAccessToken, refreshAccessToken } from './auth';

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
  body?: Record<string, unknown>;
  token?: string | null;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = 'GET', body, token } = options;
  const authToken = token ?? getAccessToken();
  const makeRequest = (access: string | null) =>
    fetch(`${API_BASE_URL}${path}`, {
      method,
      headers: {
        ...(body ? { 'Content-Type': 'application/json' } : {}),
        ...(access ? { Authorization: `Bearer ${access}` } : {}),
      },
      body: body ? JSON.stringify(body) : undefined,
      credentials: 'include',
    });

  let response = await makeRequest(authToken ?? null);

  if (response.status === 401 && !token) {
    const refreshed = await refreshAccessToken();
    if (refreshed) {
      response = await makeRequest(refreshed);
    }
  }

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
  getProfile: (token: string) =>
     // Assuming specific backend endpoint for profile.
     // In backend user router: @router.get("/myemail") returns user.
     request<UserProfile>('/myemail', { token }),
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
  createPost: (token: string, body: string, imageUrl?: string) =>
    request<Post>('/post', {
      method: 'POST',
      body: { body, image_url: imageUrl },
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

    return response.json() as Promise<{
      filename: string;
      predictions: { label: string; score_percent: number }[];
    }>;
  },
  predictFoodBatch: async (files: File[]) => {
    const form = new FormData();
    files.forEach((file) => form.append('files', file));

    const response = await fetch(`${API_BASE_URL}/food-vision/predict-batch`, {
      method: 'POST',
      body: form,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const message = errorBody?.detail || response.statusText;
      throw new Error(message);
    }

    return response.json() as Promise<{
      results: { filename: string; prediction: { label: string; score_percent: number } }[];
    }>;
  },
  predictFoodZip: async (file: File) => {
    const form = new FormData();
    form.append('file', file);

    const response = await fetch(`${API_BASE_URL}/food-vision/predict-zip`, {
      method: 'POST',
      body: form,
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      const message = errorBody?.detail || response.statusText;
      throw new Error(message);
    }

    return response.json() as Promise<{
      results: { filename: string; prediction: { label: string; score_percent: number } }[];
    }>;
  },
  uploadFile: async (file: File) => {
    const form = new FormData();
    form.append('file', file);
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: form,
    });
    if (!response.ok) throw new Error('Upload failed');
    return response.json() as Promise<{ status: string; filename: string }>;
  },
  deletePost: (token: string, postId: number) =>
    request<{ status: string }>(`/post/${postId}`, {
      method: 'DELETE',
      token,
    }),
  deleteAccount: (token: string) =>
    request<{ status: string }>('/delete', {
      method: 'DELETE',
      token,
    }),
};
