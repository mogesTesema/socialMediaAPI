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
    <Card variant="purple" className="space-y-4 slide-in-up">
      <div className="flex justify-between items-start">
         <div className="flex items-center gap-2">
           <div className="h-8 w-8 rounded-full bg-gradient-to-br from-accent-purple/40 to-accent-pink/40 flex items-center justify-center text-xs font-bold">
             #{post.id}
           </div>
           <p className="text-sm text-slate-400">Post</p>
         </div>
         {isOwner && (
            <Button tone="pink" onClick={handleDelete} className="text-xs px-3 py-2 min-h-9">
               Delete Post
            </Button>
         )}
      </div>

      <div className="space-y-3">
        <p className="text-base leading-relaxed text-slate-100 whitespace-pre-wrap font-medium">{post.body}</p>
        {post.image_url && (
          <div className="overflow-hidden rounded-2xl border border-accent-purple/50 mt-2 shadow-[0_12px_24px_-6px_rgba(167,139,250,0.2)]">
            <img
              src={post.image_url}
              alt="Post attachment"
              className="h-64 w-full object-cover hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                 (e.target as HTMLImageElement).style.display = 'none';
              }}
            />
          </div>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2 pt-2">
        <Button tone="emerald" onClick={handleLike} className="text-xs px-3 py-2 min-h-9">
          👍 Like ({likes})
        </Button>
        <Button
          tone="cyan"
          onClick={() => setShowComments((prev) => !prev)}
          className="text-xs px-3 py-2 min-h-9"
        >
          💬 {showComments ? 'Hide' : 'Show'} Comments
        </Button>
        {status && <span className="text-xs text-accent-pink/70 font-medium">{status}</span>}
      </div>

      {showComments && <CommentList postId={post.id} />}
    </Card>
  );
}
