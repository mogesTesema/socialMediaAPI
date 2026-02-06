import { useState } from 'react';
import { AuthLayout } from './AuthLayout';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { api } from '../lib/api';
import { Link } from 'react-router-dom';

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [statusTone, setStatusTone] = useState<'success' | 'error' | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    setStatus(null);
    setStatusTone(null);
    try {
      const response = await api.requestPasswordReset(email);
      setStatus(response.status ?? 'If the email exists, a reset link has been sent.');
      setStatusTone('success');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to send reset email';
      setStatus(message);
      setStatusTone('error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthLayout
      title="Reset password"
      subtitle="Send a password reset link to the account email."
    >
      <Input
        label="Email"
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
      />
      <Button onClick={handleSubmit} disabled={!email || isLoading}>
        {isLoading ? 'Sending...' : 'Send reset link'}
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
