import { useState } from 'react';
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
  const [isLoading, setIsLoading] = useState(false);

  const canPost = Boolean(accessToken);

  const handleSubmit = async () => {
    if (!accessToken) return;
    setIsLoading(true);
    setStatus(null);
    try {
      const post = await api.createPost(accessToken, body);
      onPostCreated(post);
      setBody('');
      setStatus('Post published.');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Failed to post';
      setStatus(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="space-y-4">
      <div>
        <h3 className="text-lg font-semibold text-white">Create a post</h3>
        <p className="text-sm text-slate-400">Share the latest food updates.</p>
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
          <span className="text-xs text-slate-500">Sign in to publish posts.</span>
        )}
      </div>
      {status && (
        <div className="rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-xs text-slate-200">
          {status}
        </div>
      )}
    </Card>
  );
}
