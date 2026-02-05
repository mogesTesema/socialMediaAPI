import { useState } from 'react';
import { AuthLayout } from './AuthLayout';
import { Input } from '../components/Input';
import { Button } from '../components/Button';
import { api } from '../lib/api';
import { Link } from 'react-router-dom';

export function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    setIsLoading(true);
    setStatus(null);
    try {
      const response = await api.requestPasswordReset(email);
      setStatus(response.status ?? 'If the email exists, a reset link has been sent.');
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unable to send reset email';
      setStatus(message);
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
