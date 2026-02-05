export interface AuthResponse {
  status?: string;
  'access token'?: string;
  'access token:'?: string;
}

export interface UserProfile {
  id?: number;
  email: string;
  confirmed?: boolean;
}

export interface Post {
  id: number;
  user_id: number;
  body: string;
  image_url?: string | null;
  likes?: number;
}

export interface Comment {
  id: number;
  post_id: number;
  user_id: number;
  body: string;
}

export interface PostWithComments {
  post: Post;
  comment: Comment[];
}

export type PostSorting = 'new' | 'old' | 'likes';
