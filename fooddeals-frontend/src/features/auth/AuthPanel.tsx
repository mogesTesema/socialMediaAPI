import { useState } from 'react';
import { api } from '../../lib/api';
import { Button } from '../../components/Button';
import { Card } from '../../components/Card';
import { Input } from '../../components/Input';
import { useAuth } from './AuthContext';

export function AuthPanel() {
  const { accessToken, setAccessToken, clearSession } = useAuth();
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    setStatus(null);
    try {
      const response =
        mode === 'login'
          ? await api.login(email, password)
          : await api.register(email, password);
      const token = response['access token'] || response['access token:'] || null;
      if (token) {
        setAccessToken(token);
        setStatus('Access token stored. You are signed in.');
      } else {
        setStatus('Request completed. Check your email for confirmation.');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to authenticate';
      setStatus(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-xl font-semibold text-white">{mode === 'login' ? 'Sign in' : 'Create account'}</h3>
          <p className="text-sm text-slate-400">
            {mode === 'login'
              ? 'Use your credentials to access the API.'
              : 'Register to unlock posting, likes, and comments.'}
          </p>
        </div>
        {accessToken && (
          <Button tone="ghost" onClick={clearSession}>
            Sign out
          </Button>
        )}
      </div>

      <div className="space-y-4">
        <Input
          label="Email"
          type="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
          placeholder="you@fooddeals.com"
        />
        <Input
          label="Password"
          type="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          placeholder="••••••••"
        />
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={handleSubmit} disabled={isLoading || !email || !password}>
          {isLoading ? 'Working...' : mode === 'login' ? 'Sign in' : 'Register'}
        </Button>
        <Button
          tone="secondary"
          onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
        >
          {mode === 'login' ? 'Need an account?' : 'Already have an account?'}
        </Button>
      </div>

      {accessToken && (
        <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 px-4 py-3 text-xs text-emerald-200">
          Access token set. You can create posts and interact with content.
        </div>
      )}

      {status && (
        <div className="rounded-2xl border border-slate-700 bg-slate-900/70 px-4 py-3 text-xs text-slate-200">
          {status}
        </div>
      )}
    </Card>
  );
}
