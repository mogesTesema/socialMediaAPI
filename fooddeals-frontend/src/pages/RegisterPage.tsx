import { useState } from 'react';
import { AuthLayout } from './AuthLayout';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { api } from '../lib/api';
import { Link } from 'react-router-dom';

export function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [statusTone, setStatusTone] = useState<'success' | 'error' | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    setStatus(null);
    setStatusTone(null);
    try {
      const response = await api.register(email, password);
      const token = response['access token'] || response['access token:'] || null;
      if (token) {
        setStatus('Account created. Please check your email to confirm.');
      } else {
        setStatus('Account created. Please check your email to confirm.');
      }
      setStatusTone('success');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to register';
      setStatus(message);
      setStatusTone('error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Create account"
      subtitle="Set up FoodDeals access for your team."
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
      <Button onClick={handleSubmit} disabled={!email || !password || isLoading}>
        {isLoading ? 'Creating...' : 'Create account'}
      </Button>
      <p className="text-xs text-amber-200/70">
        Already have access? <Link className="text-emerald-200" to="/auth/login">Sign in</Link>
      </p>
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
    </AuthLayout>
  );
}
