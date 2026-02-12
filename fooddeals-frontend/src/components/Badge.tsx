import { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  className?: string;
}

export function Badge({ children, className = '' }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center gap-2 rounded-full border border-primary-500/40 bg-primary-500/10 px-3 py-1.5 text-xs font-semibold uppercase tracking-[0.15em] text-primary-200/90 backdrop-blur-sm hover:bg-primary-500/15 transition-colors duration-200 ${className}`}
    >
      {children}
    </span>
  );
}
