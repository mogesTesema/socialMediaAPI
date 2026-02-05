import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className = '' }: CardProps) {
  return (
    <div
      className={`rounded-3xl border border-slate-800 bg-slate-900/60 p-6 shadow-[0_20px_60px_-40px_rgba(15,23,42,0.9)] ${className}`}
    >
      {children}
    </div>
  );
}
