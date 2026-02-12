import { useEffect, useMemo, useState } from 'react';
import { api } from '../../lib/api';
import type { Post, PostSorting } from '../../lib/types';
import { PostCard } from './PostCard';
import { Button } from '../../components/Button';

interface PostListProps {
  searchTerm: string;
  prependPosts?: Post[];
  refreshKey?: number;
}

export function PostList({ searchTerm, prependPosts = [], refreshKey = 0 }: PostListProps) {
  const [posts, setPosts] = useState<Post[]>([]);
  const [sorting, setSorting] = useState<PostSorting>('new');
  const [status, setStatus] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    setStatus(null);
    api
      .getPosts(sorting)
      .then((data) => {
        if (isMounted) setPosts(data);
      })
      .catch((error) => {
        if (isMounted) {
          setStatus(error instanceof Error ? error.message : 'Unable to load posts');
        }
      });
    return () => {
      isMounted = false;
    };
  }, [sorting, refreshKey]);

  const handleDelete = (id: number) => {
    setPosts((prev) => prev.filter((p) => p.id !== id));
  }

  const filteredPosts = useMemo(() => {
    const merged = sorting === 'new' ? [...prependPosts, ...posts] : posts;
    const unique = merged.filter(
      (post, index, array) => array.findIndex((item) => item.id === post.id) === index,
    );
    if (!searchTerm.trim()) return unique;
    const term = searchTerm.toLowerCase();
    return unique.filter((post) => post.body.toLowerCase().includes(term));
  }, [posts, prependPosts, searchTerm, sorting]);

  return (
    <section className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-700/50">
        <div>
          <h3 className="text-2xl font-bold text-slate-100">Latest Posts</h3>
          <p className="text-slate-400 text-sm mt-1">Sort and discover content from the community</p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {(['new', 'old', 'likes'] as PostSorting[]).map((option) => (
            <Button
              key={option}
              tone={sorting === option ? 'primary' : 'secondary'}
              onClick={() => setSorting(option)}
              className="text-xs px-3 py-2 min-h-9"
            >
              {option === 'likes' ? '❤️ Most liked' : option === 'new' ? '⏰ Newest' : '📅 Oldest'}
            </Button>
          ))}
        </div>
      </div>

      {status && (
        <div className="rounded-2xl border border-accent-pink/50 bg-accent-pink/10 px-4 py-3 text-xs text-accent-pink/90 font-medium">
          ✕ {status}
        </div>
      )}

      <div className="space-y-4">
        {filteredPosts.length === 0 ? (
          <div className="rounded-3xl border border-slate-600/50 bg-slate-800/40 p-8 text-center">
            <p className="text-2xl mb-2">📭</p>
            <p className="text-slate-400">No posts match your search yet.</p>
            <p className="text-slate-500 text-sm mt-1">Be the first to share something great!</p>
          </div>
        ) : (
          filteredPosts.map((post) => (
            <div key={post.id} className="animate-in fade-in duration-300">
              <PostCard post={post} onDelete={handleDelete} />
            </div>
          ))
        )}
      </div>
    </section>
  );
}
