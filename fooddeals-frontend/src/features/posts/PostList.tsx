import { useEffect, useMemo, useState } from 'react';
import { api } from '../../lib/api';
import type { Post, PostSorting } from '../../lib/types';
import { PostCard } from './PostCard';
import { SectionHeader } from '../../components/SectionHeader';
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
          <div className="rounded-3xl border border-amber-400/30 bg-amber-500/5 p-8 text-sm text-amber-200/80">
            No posts yet. Once users create posts they will appear here.
          </div>
        ) : (
          filteredPosts.map((post) => <PostCard key={post.id} post={post} onDelete={handleDelete} />)
        )}
      </div>
    </section>
  );
}
