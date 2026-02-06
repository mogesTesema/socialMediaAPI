import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div
      className={`rounded-3xl border border-sky-500/20 bg-emerald-500/5 p-6 shadow-[0_20px_60px_-40px_rgba(16,185,129,0.35)] ${className}`}
    >
      {children}
    </div>
  );
}
