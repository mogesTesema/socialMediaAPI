import { useEffect, useMemo, useState } from 'react';
import { api } from '../../lib/api';
import type { Post, PostSorting } from '../../lib/types';
import { PostCard } from './PostCard';
import { SectionHeader } from '../../components/SectionHeader';
import { Button } from '../../components/Button';

interface PostListProps {
  searchTerm: string;
  prependPosts?: Post[];
}

export function PostList({ searchTerm, prependPosts = [] }: PostListProps) {
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
  }, [sorting]);

  const filteredPosts = useMemo(() => {
    const merged = [...prependPosts, ...posts];
    if (!searchTerm.trim()) return merged;
    const term = searchTerm.toLowerCase();
    return merged.filter((post) => post.body.toLowerCase().includes(term));
  }, [posts, prependPosts, searchTerm]);

  return (
    <section className="space-y-6">
      <SectionHeader
        title="Content feed"
        subtitle="Review posts, likes, and comments as they land in FoodDeals."
        action={
          <div className="flex flex-wrap items-center gap-2">
            {(['new', 'old', 'likes'] as PostSorting[]).map((option) => (
              <Button
                key={option}
                tone={sorting === option ? 'primary' : 'secondary'}
                onClick={() => setSorting(option)}
              >
                {option === 'likes' ? 'Most liked' : option === 'new' ? 'Newest' : 'Oldest'}
              </Button>
            ))}
          </div>
        }
      />

      {status && (
        <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 px-4 py-3 text-xs text-rose-200">
          {status}
        </div>
      )}

      <div className="space-y-6">
        {filteredPosts.length === 0 ? (
          <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 text-sm text-slate-400">
            No posts yet. Once users create posts they will appear here.
          </div>
        ) : (
          filteredPosts.map((post) => <PostCard key={post.id} post={post} />)
        )}
      </div>
    </section>
  );
}
