import { useState } from 'react';
import { SearchBar } from '../features/search/SearchBar';
import { PostComposer } from '../features/posts/PostComposer';
import { PostList } from '../features/posts/PostList';
import type { Post } from '../lib/types';

export function DashboardPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [newPosts, setNewPosts] = useState<Post[]>([]);
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-slate-700/50">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary-400 via-accent-emerald to-accent-cyan bg-clip-text text-transparent">
            Content Feed
          </h1>
          <p className="text-slate-400 mt-2">
            Browse posts, engage with the community, and share your food deals
          </p>
        </div>
      </div>

      <section className="grid gap-8 lg:grid-cols-[0.65fr_1.35fr]">
        <aside className="space-y-6 h-fit">
          <SearchBar value={searchTerm} onChange={setSearchTerm} />
          <PostComposer
            onPostCreated={(post) => {
              setNewPosts((prev) => [post, ...prev]);
              setRefreshKey((prev) => prev + 1);
            }}
          />
          {newPosts.length > 0 && (
            <div className="rounded-3xl border border-accent-cyan/50 bg-accent-cyan/10 p-4 text-xs text-accent-cyan/90 font-medium shadow-[0_12px_24px_-6px_rgba(6,182,212,0.15)] slide-in-up">
              <div className="flex items-center gap-2 mb-1">
                <span className="text-lg">✨</span>
                <span className="font-bold">{newPosts.length} new post{newPosts.length > 1 ? 's' : ''}</span>
              </div>
              <span className="text-accent-cyan/70">Added this session</span>
            </div>
          )}
        </aside>

        <article>
          <PostList
            searchTerm={searchTerm}
            prependPosts={newPosts}
            refreshKey={refreshKey}
          />
        </article>
      </section>
    </div>
  );
}
