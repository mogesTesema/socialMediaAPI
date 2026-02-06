import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  tone?: 'primary' | 'secondary' | 'ghost';
}

const toneStyles: Record<NonNullable<ButtonProps['tone']>, string> = {
  primary:
    'bg-brand-500 text-emerald-950 shadow-[0_16px_34px_-18px_rgba(16,185,129,0.9)] hover:bg-brand-400 focus-visible:outline-brand-300',
  secondary:
    'border border-amber-400/40 bg-amber-400/15 text-amber-50 hover:bg-amber-400/25 focus-visible:outline-amber-300',
  ghost:
    'border border-sky-400/40 bg-sky-500/10 text-slate-100 hover:bg-sky-500/20 focus-visible:outline-sky-300',
};

export function Button({
  tone = 'primary',
  className = '',
  type = 'button',
  ...props
}: ButtonProps) {
  return (
    <button
      type={type}
      className={`inline-flex min-h-11 items-center justify-center gap-2 rounded-2xl px-5 py-3 text-base font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-60 ${
        toneStyles[tone]
      } ${className}`}
      {...props}
    />
  );
}
