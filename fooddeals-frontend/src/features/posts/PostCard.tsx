import { useState } from 'react';
import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { api } from '../../lib/api';
import type { Post } from '../../lib/types';
import { useAuth } from '../auth/AuthContext';
import { CommentList } from './CommentList';

interface PostCardProps {
  post: Post;
  onDelete?: (id: number) => void;
}

export function PostCard({ post, onDelete }: PostCardProps) {
  const { accessToken, user } = useAuth();
  const [likes, setLikes] = useState(post.likes ?? 0);
  const [showComments, setShowComments] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  const isOwner = user?.id === post.user_id;

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

  const handleDelete = async () => {
     if (!accessToken || !isOwner) return;
     if (!window.confirm('Are you sure you want to delete this post?')) return;
     
     try {
       await api.deletePost(accessToken, post.id);
       onDelete?.(post.id);
     } catch(error) {
       const message = error instanceof Error ? error.message : 'Unable to delete post';
       setStatus(message);
     }
  };

  return (
    <Card className="space-y-4 border-violet-500/30 bg-violet-500/5">
      <div className="flex justify-between items-start">
         <p className="text-sm text-amber-200/70">Post #{post.id}</p>
         {isOwner && (
            <Button tone="secondary" onClick={handleDelete} className="bg-red-500/10 hover:bg-red-500/20 text-red-200 border-red-500/30">
               Delete
            </Button>
         )}
      </div>

      <div className="space-y-2">
        <p className="text-base text-white whitespace-pre-wrap">{post.body}</p>
        {post.image_url && (
          <div className="overflow-hidden rounded-2xl border border-sky-500/30 mt-2">
            <img
              src={post.image_url}
              alt="Post attachment"
              className="h-64 w-full object-cover"
              onError={(e) => {
                 (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-3 pt-2">
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
