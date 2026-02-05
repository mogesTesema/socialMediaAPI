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
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!token) {
      setStatus('Reset token is missing.');
      return;
    }
    if (password !== confirmPassword) {
      setStatus('Passwords do not match.');
      return;
    }
    setIsLoading(true);
    setStatus(null);
    try {
      const response = await api.resetPassword(token, password);
      setStatus(response.status ?? 'Password reset successfully. Redirecting...');
      setTimeout(() => navigate('/auth/login'), 1200);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to reset password';
      setStatus(message);
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
      <p className="text-xs text-slate-400">
        Back to <Link className="text-brand-200" to="/auth/login">Sign in</Link>
      </p>
      {status && (
        <div className="rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-xs text-slate-200">
          {status}
        </div>
      )}
    </AuthLayout>
  );
}
