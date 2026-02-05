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
    <div className="space-y-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-semibold text-white">Content dashboard</h2>
          <p className="text-sm text-slate-400">
            Review posts, likes, and comments as they land in FoodDeals.
          </p>
        </div>
      </div>

      <section className="grid gap-8 lg:grid-cols-[0.7fr_1.3fr]">
        <div className="space-y-6">
          <SearchBar value={searchTerm} onChange={setSearchTerm} />
          <PostComposer
            onPostCreated={(post) => {
              setNewPosts((prev) => [post, ...prev]);
              setRefreshKey((prev) => prev + 1);
            }}
          />
          {newPosts.length > 0 && (
            <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-4 text-xs text-slate-200">
              {newPosts.length} new post{newPosts.length > 1 ? 's' : ''} added this
              session.
            </div>
          )}
        </div>

        <PostList
          searchTerm={searchTerm}
          prependPosts={newPosts}
          refreshKey={refreshKey}
        />
      </section>
    </div>
  );
}
