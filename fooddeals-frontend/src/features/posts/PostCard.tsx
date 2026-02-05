import { useState } from 'react';
import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { api } from '../../lib/api';
import type { Post } from '../../lib/types';
import { useAuth } from '../auth/AuthContext';
import { CommentList } from './CommentList';

interface PostCardProps {
  post: Post;
}

export function PostCard({ post }: PostCardProps) {
  const { accessToken } = useAuth();
  const [likes, setLikes] = useState(post.likes ?? 0);
  const [showComments, setShowComments] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const handleLike = async () => {
    if (!accessToken) {
      setStatus('Sign in to like posts.');
      return;
    }
    setStatus(null);
    try {
      await api.likePost(accessToken, post.id);
      setLikes((prev) => prev + 1);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to like post';
      setStatus(message);
    }
  };

  return (
    <Card className="space-y-4">
      <div className="space-y-2">
        <p className="text-sm text-slate-400">Post #{post.id}</p>
        <p className="text-base text-white">{post.body}</p>
        {post.image_url && (
          <div className="overflow-hidden rounded-2xl border border-slate-800">
            <img
              src={post.image_url}
              alt="Post"
              className="h-48 w-full object-cover"
            />
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <Button tone="secondary" onClick={handleLike}>
          👍 Like ({likes})
        </Button>
        <Button
          tone="ghost"
          onClick={() => setShowComments((prev) => !prev)}
        >
          {showComments ? 'Hide comments' : 'Show comments'}
        </Button>
        {status && <span className="text-xs text-rose-300">{status}</span>}
      </div>

      {showComments && <CommentList postId={post.id} />}
    </Card>
  );
}
