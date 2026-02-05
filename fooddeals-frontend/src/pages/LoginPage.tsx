import { useState } from 'react';
import { AuthLayout } from './AuthLayout';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { api } from '../lib/api';
import { useAuth } from '../features/auth/AuthContext';
import { setAccessToken } from '../lib/auth';
import { Link, useNavigate } from 'react-router-dom';

export function LoginPage() {
  const { setAccessToken } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    setStatus(null);
    try {
      const response = await api.login(email, password);
      const token = response['access token'] || response['access token:'] || null;
      if (token) {
        setAccessToken(token);
        navigate('/dashboard');
      } else {
        setStatus('Login succeeded but token missing.');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to login';
      setStatus(message);
      setAccessToken(null);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Welcome back"
      subtitle="Sign in to manage posts, comments, and insights."
    >
      <Input
        label="Email"
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <Input
        label="Password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />
      <div className="flex flex-wrap items-center gap-3">
        <Button onClick={handleSubmit} disabled={!email || !password || isLoading}>
          {isLoading ? 'Signing in...' : 'Sign in'}
        </Button>
        <Link to="/auth/forgot" className="text-xs text-slate-400 hover:text-slate-200">
          Forgot password?
        </Link>
      </div>
      <p className="text-xs text-slate-400">
        New here? <Link className="text-brand-200" to="/auth/register">Create account</Link>
      </p>
      {status && (
        <div className="rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-xs text-slate-200">
          {status}
        </div>
      )}
    </AuthLayout>
  );
}
