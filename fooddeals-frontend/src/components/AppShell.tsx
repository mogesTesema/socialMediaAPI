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
  { label: 'Live Video', to: '/video-chat' },
];

export function AppShell({ children }: AppShellProps) {
  const { accessToken, user } = useAuth();

  return (
    <div className="min-h-screen text-slate-100">
      <header className="border-b border-slate-700/50 bg-gradient-to-r from-slate-900/80 via-slate-900/70 to-primary-950/70 backdrop-blur-md sticky top-0 z-50">
        <Container>
          <div className="flex flex-wrap items-center justify-between gap-4 py-6">
            <NavLink to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity duration-300">
              <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-accent-emerald/20 to-accent-cyan/20 text-2xl shadow-[0_8px_16px_-4px_rgba(16,185,129,0.2)]">
                🍲
              </div>
              <div>
                <p className="text-sm font-bold uppercase tracking-[0.3em] bg-gradient-to-r from-accent-emerald to-accent-cyan bg-clip-text text-transparent">
                  FoodDeals
                </p>
                <p className="text-xs text-slate-400">Community Platform</p>
              </div>
            </NavLink>
            <div className="flex flex-wrap items-center gap-2 sm:gap-3">
              <Badge>React + FastAPI</Badge>
              <Badge className="bg-accent-cyan/10 text-accent-cyan/90">Modern UI</Badge>
              {accessToken && (
                 <NavLink
                   to="/settings"
                   className="rounded-full border border-primary-500/40 bg-primary-500/10 px-4 py-2.5 text-xs font-semibold text-primary-100 transition-all duration-300 hover:bg-primary-500/20 hover:border-primary-400"
                 >
                   {user?.email || 'Account'}
                 </NavLink>
              )}
            </div>
          </div>
          <nav className="flex flex-wrap gap-2 pb-4">
            {navItems.map((item, idx) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) => {
                  const colors = ['from-primary-500', 'from-accent-emerald', 'from-accent-purple', 'from-accent-cyan'];
                  const color = colors[idx % colors.length];
                  return `rounded-full px-4 py-2.5 text-sm font-semibold uppercase tracking-[0.15em] transition-all duration-300 text-nowrap ${
                    isActive
                      ? `bg-gradient-to-r ${color} to-accent-cyan/40 text-white shadow-[0_8px_16px_-4px_rgba(0,0,0,0.3)]`
                      : 'border border-slate-600/50 text-slate-300 hover:border-primary-500/50 hover:bg-slate-700/30 hover:text-slate-100'
                  }`;
                }}
              >
                {item.label}
              </NavLink>
            ))}
            {!accessToken && (
              <NavLink
                to="/auth/login"
                className={({ isActive }) =>
                  `rounded-full px-4 py-2.5 text-sm font-semibold uppercase tracking-[0.15em] transition-all duration-300 ${
                    isActive
                      ? 'bg-gradient-to-r from-accent-emerald to-accent-cyan text-white shadow-[0_8px_16px_-4px_rgba(0,0,0,0.3)]'
                      : 'border border-slate-600/50 text-slate-300 hover:border-accent-emerald/50 hover:bg-slate-700/30 hover:text-emerald-100'
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
