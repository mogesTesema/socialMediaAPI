import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  variant?: 'primary' | 'emerald' | 'purple' | 'pink' | 'orange' | 'cyan' | 'default';
}

const variantStyles: Record<NonNullable<CardProps['variant']>, string> = {
  primary: 'border-primary-600/40 bg-primary-950/30 shadow-[0_20px_60px_-40px_rgba(59,130,246,0.3)]',
  emerald: 'border-accent-emerald/40 bg-accent-emerald/5 shadow-[0_20px_60px_-40px_rgba(16,185,129,0.25)]',
  purple: 'border-accent-purple/40 bg-accent-purple/5 shadow-[0_20px_60px_-40px_rgba(167,139,250,0.25)]',
  pink: 'border-accent-pink/40 bg-accent-pink/5 shadow-[0_20px_60px_-40px_rgba(244,114,182,0.25)]',
  orange: 'border-accent-orange/40 bg-accent-orange/5 shadow-[0_20px_60px_-40px_rgba(249,115,22,0.25)]',
  cyan: 'border-accent-cyan/40 bg-accent-cyan/5 shadow-[0_20px_60px_-40px_rgba(6,182,212,0.25)]',
  default: 'border-slate-700/50 bg-slate-800/40 shadow-[0_20px_60px_-40px_rgba(100,116,139,0.2)]',
};

export function Card({ children, className = '', variant = 'default' }: CardProps) {
  return (
    <div
      className={`rounded-3xl border p-6 backdrop-blur-sm transition-all duration-300 hover:shadow-[0_25px_70px_-35px_rgba(59,130,246,0.4)] ${variantStyles[variant]} ${className}`}
    >
      {children}
    </div>
  );
}
