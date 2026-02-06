import { useEffect, useState } from 'react';
import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { Input } from '../../components/Input';
import { api } from '../../lib/api';
import { useAuth } from '../auth/AuthContext';
import type { Post } from '../../lib/types';

interface PostComposerProps {
  onPostCreated: (post: Post) => void;
}

export function PostComposer({ onPostCreated }: PostComposerProps) {
  const { accessToken } = useAuth();
  const [body, setBody] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [statusTone, setStatusTone] = useState<'success' | 'error' | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const canPost = Boolean(accessToken);

  const handleSubmit = async () => {
    if (!accessToken) return;
    setIsLoading(true);
    setStatus(null);
    setStatusTone(null);
    try {
      const post = await api.createPost(accessToken, body);
      onPostCreated(post);
      setBody('');
      setStatus('Post published.');
      setStatusTone('success');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to post';
      setStatus(message);
      setStatusTone('error');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (!status) return undefined;
    const timer = window.setTimeout(() => {
      setStatus(null);
      setStatusTone(null);
    }, 2500);
    return () => window.clearTimeout(timer);
  }, [status]);

  return (
    <Card className="space-y-4 border-emerald-500/30 bg-emerald-500/5">
      <div>
        <h3 className="text-lg font-semibold text-white">Create a post</h3>
        <p className="text-sm text-amber-200/70">Share the latest food updates.</p>
      </div>
      <Input
        label="Post"
        placeholder="Share a deal or dish insight..."
        value={body}
        onChange={(event) => setBody(event.target.value)}
        disabled={!canPost}
      />
      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={handleSubmit} disabled={!canPost || !body || isLoading}>
          {isLoading ? 'Publishing...' : 'Publish'}
        </Button>
        {!canPost && (
          <span className="text-xs text-amber-200/60">Sign in to publish posts.</span>
        )}
      </div>
      {status && (
        <div
          className={`rounded-2xl border px-4 py-2 text-xs ${
            statusTone === 'success'
              ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-200'
              : 'border-rose-500/40 bg-rose-500/10 text-rose-200'
          }`}
        >
          {status}
        </div>
      )}
    </Card>
  );
}
