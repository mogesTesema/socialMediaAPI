import { NavLink } from 'react-router-dom';
import { Container } from './Container';
import { Badge } from './Badge';
import { useAuth } from '../features/auth/AuthContext';

interface AppShellProps {
  children: React.ReactNode;
}

const navItems = [
  { label: 'Home', to: '/' },
  { label: 'Dashboard', to: '/dashboard' },
  { label: 'Food Vision', to: '/food-vision' },
];

export function AppShell({ children }: AppShellProps) {
  const { accessToken, clearSession } = useAuth();

  return (
    <div className="min-h-screen text-slate-100">
      <header className="border-b border-sky-500/30">
        <Container>
          <div className="flex flex-wrap items-center justify-between gap-4 py-6">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-brand-500/15 text-brand-200">
                🍲
              </div>
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.3em] text-amber-100">
                  FoodDeals
                </p>
                <p className="text-xs text-amber-200/70">Operations Console</p>
              </div>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <Badge>FastAPI + React</Badge>
              <Badge className="bg-emerald-500/10 text-emerald-200">Production UI</Badge>
              {accessToken && (
                <button
                  className="rounded-full border border-amber-400/40 bg-amber-500/10 px-4 py-2.5 text-xs font-semibold text-amber-100 transition hover:bg-amber-500/20"
                  onClick={clearSession}
                >
                  Sign out
                </button>
              )}
            </div>
          </div>
          <nav className="flex flex-wrap gap-3 pb-4">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2.5 text-sm font-semibold uppercase tracking-[0.2em] transition ${
                    isActive
                      ? 'bg-brand-500/20 text-brand-200'
                      : 'border border-sky-500/30 text-slate-200 hover:border-brand-500/40 hover:text-brand-100'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
            {!accessToken && (
              <NavLink
                to="/auth/login"
                className={({ isActive }) =>
                  `rounded-full px-4 py-2.5 text-sm font-semibold uppercase tracking-[0.2em] transition ${
                    isActive
                      ? 'bg-emerald-500/20 text-emerald-200'
                      : 'border border-sky-500/30 text-slate-200 hover:border-emerald-500/40 hover:text-emerald-100'
                  }`
                }
              >
                Sign in
              </NavLink>
            )}
          </nav>
        </Container>
      </header>

      <main className="py-12">
        <Container>{children}</Container>
      </main>
    </div>
  );
}
