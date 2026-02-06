import { Card } from '../components/Card';

interface AuthLayoutProps {
  title: string;
  subtitle: string;
  children: React.ReactNode;
}

export function AuthLayout({ title, subtitle, children }: AuthLayoutProps) {
  return (
    <div className="mx-auto flex w-full max-w-lg flex-col gap-6">
      <div>
        <h2 className="text-3xl font-semibold text-white">{title}</h2>
        <p className="mt-2 text-sm text-amber-200/70">{subtitle}</p>
      </div>
      <Card className="space-y-6 border-indigo-500/30 bg-indigo-500/5">
        {children}
      </Card>
    </div>
  );
}
