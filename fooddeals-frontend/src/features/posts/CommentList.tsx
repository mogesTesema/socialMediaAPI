import { useEffect, useState } from 'react';
import { api } from '../../lib/api';
import type { Comment, PostWithComments } from '../../lib/types';
import { Button } from '../../components/Button';
import { Input } from '../../components/Input';
import { useAuth } from '../auth/AuthContext';

interface CommentListProps {
  postId: number;
}

export function CommentList({ postId }: CommentListProps) {
  const { accessToken } = useAuth();
  const [comments, setComments] = useState<Comment[]>([]);
  const [body, setBody] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    api
      .getPostComments(postId)
      .then((data: PostWithComments) => {
        if (isMounted) {
          setComments(data.comment ?? []);
        }
      })
      .catch(() => {
        if (isMounted) {
          setComments([]);
        }
      });
    return () => {
      isMounted = false;
    };
  }, [postId]);

  const handleAddComment = async () => {
    if (!accessToken) return;
    setIsLoading(true);
    setStatus(null);
    try {
      const newComment = await api.addComment(accessToken, postId, body);
      setComments((prev) => [newComment, ...prev]);
      setBody('');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to add comment';
      setStatus(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-4 rounded-2xl border border-accent-pink/40 bg-accent-pink/5 p-4 mt-4 backdrop-blur-sm">
      <div className="flex items-center justify-between border-b border-accent-pink/30 pb-3">
        <h4 className="font-bold text-accent-pink/90 flex items-center gap-2">
          <span>💬</span> Comments ({comments.length})
        </h4>
      </div>

      <div className="space-y-2 max-h-64 overflow-y-auto">
        {comments.length === 0 ? (
          <p className="text-sm text-slate-400 italic py-4 text-center">Be the first to comment!</p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="rounded-xl border border-accent-orange/30 bg-accent-orange/5 p-3 text-sm text-slate-100 hover:bg-accent-orange/10 transition-all duration-200">
              <p className="leading-relaxed">{comment.body}</p>
              <p className="text-xs text-slate-500 mt-1">Just now</p>
            </div>
          ))
        )}
      </div>

      <div className="space-y-2 border-t border-accent-pink/30 pt-3">
        <Input
          label=""
          value={body}
          onChange={(event) => setBody(event.target.value)}
          disabled={!accessToken}
          placeholder={accessToken ? 'Write a thoughtful comment...' : 'Sign in to comment'}
        />
        <div className="flex items-center gap-2">
          <Button
            tone="pink"
            onClick={handleAddComment}
            disabled={!accessToken || !body || isLoading}
            className="text-xs px-3 py-2 min-h-9"
          >
            {isLoading ? '⏳ Sending...' : '📤 Comment'}
          </Button>
          {status && <span className="text-xs text-accent-pink/70 font-medium">{status}</span>}
        </div>
      </div>
    </div>
  );
}
