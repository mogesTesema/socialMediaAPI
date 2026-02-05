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
    <div className="space-y-3 rounded-2xl border border-slate-800 bg-slate-950/60 p-4">
      <div className="flex items-center justify-between">
        <p className="text-sm font-semibold text-slate-200">Comments</p>
        <span className="text-xs text-slate-500">{comments.length}</span>
      </div>

      <div className="space-y-3">
        {comments.length === 0 ? (
          <p className="text-xs text-slate-500">No comments yet.</p>
        ) : (
          comments.map((comment) => (
            <div key={comment.id} className="rounded-xl border border-slate-800 bg-slate-900/40 p-3 text-xs text-slate-200">
              {comment.body}
            </div>
          ))
        )}
      </div>

      <div className="space-y-2">
        <Input
          label="Add comment"
          value={body}
          onChange={(event) => setBody(event.target.value)}
          disabled={!accessToken}
          placeholder={accessToken ? 'Write a comment...' : 'Sign in to comment'}
        />
        <div className="flex items-center gap-2">
          <Button
            tone="secondary"
            onClick={handleAddComment}
            disabled={!accessToken || !body || isLoading}
          >
            {isLoading ? 'Sending...' : 'Send'}
          </Button>
          {status && <span className="text-xs text-rose-300">{status}</span>}
        </div>
      </div>
    </div>
  );
}
