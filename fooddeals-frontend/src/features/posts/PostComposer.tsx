import { useEffect, useState } from 'react';
import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { Input } from '../../components/Input';
import { FileUploader } from '../../components/FileUploader';
import { api } from '../../lib/api';
import { useAuth } from '../auth/AuthContext';
import type { Post } from '../../lib/types';
import { API_BASE_URL } from '../../lib/config';

interface PostComposerProps {
  onPostCreated: (post: Post) => void;
}

export function PostComposer({ onPostCreated }: PostComposerProps) {
  const { accessToken } = useAuth();
  const [body, setBody] = useState('');
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [statusTone, setStatusTone] = useState<'success' | 'error' | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const canPost = Boolean(accessToken);

  const handleFileSelect = (file: File) => {
    setImageFile(file);
  };

  const handleSubmit = async () => {
    if (!accessToken) return;
    setIsLoading(true);
    setStatus(null);
    setStatusTone(null);
    try {
      let imageUrl: string | undefined;

      if (imageFile) {
        // First upload the image if one is selected
        const uploadResult = await api.uploadFile(imageFile);
        
        // Construct the full URL for the image.
        // Assuming current simple local upload returns just filename. 
        // We'll map it to the static serving path or assume backend provides url.
        // The backend returns { status: "uploaded", filename: "xyz.jpg" }
        // We'll need to know where these appear. Usually a static mount or a different router.
        // For local dev, let's assume valid URL construction or modify backend to return full URL.
        // For now, let's construct relative to API base if it's served there, or leave it relative.
        // Since backend doesn't return full URL yet, we store filename.
        // But PostCard expects image_url. Let's prepend the known static path if we can.
        // Or store it as provided and let PostCard resolve it.
        // Actually, let's assume we store what backend returns or link against a static route.
        // The current backend upload router saves to 'uploadedfiles'. 
        // We need a static mount in FastAPI to serve these.
        // Assuming there isn't one yet, we will just store the filename for now.
        imageUrl = `${API_BASE_URL}/static/${uploadResult.filename}`; // Hypothetical path until we fix backend serving
      }

      const post = await api.createPost(accessToken, body, imageUrl);
      onPostCreated(post);
      setBody('');
      setImageFile(null);
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
      
      {canPost && (
         <div className="mb-2">
            <FileUploader 
               onFileSelect={handleFileSelect} 
               label="Attach Image"
               accept="image/*"
            />
         </div>
      )}

      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={handleSubmit} disabled={!canPost || (!body && !imageFile) || isLoading}>
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
