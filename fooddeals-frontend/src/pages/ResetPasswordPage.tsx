import { useMemo, useState } from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { AuthLayout } from './AuthLayout';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { api } from '../lib/api';

function useQuery() {
  const { search } = useLocation();
  return useMemo(() => new URLSearchParams(search), [search]);
}

export function ResetPasswordPage() {
  const query = useQuery();
  const token = query.get('token') ?? '';
  const navigate = useNavigate();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [statusTone, setStatusTone] = useState<'success' | 'error' | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!token) {
      setStatus('Reset token is missing.');
      setStatusTone('error');
      return;
    }
    if (password !== confirmPassword) {
      setStatus('Passwords do not match.');
      setStatusTone('error');
      return;
    }
    setIsLoading(true);
    setStatus(null);
    setStatusTone(null);
    try {
      const response = await api.resetPassword(token, password);
      setStatus(response.status ?? 'Password reset successfully. Redirecting...');
      setStatusTone('success');
      setTimeout(() => navigate('/auth/login'), 1200);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to reset password';
      setStatus(message);
      setStatusTone('error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Set new password"
      subtitle="Enter a new password for this account."
    >
      <Input
        label="New password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
      />
      <Input
        label="Confirm new password"
        type="password"
        value={confirmPassword}
        onChange={(event) => setConfirmPassword(event.target.value)}
      />
      <Button onClick={handleSubmit} disabled={!password || isLoading}>
        {isLoading ? 'Resetting...' : 'Reset password'}
      </Button>
      <p className="text-xs text-amber-200/70">
        Back to <Link className="text-emerald-200" to="/auth/login">Sign in</Link>
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
