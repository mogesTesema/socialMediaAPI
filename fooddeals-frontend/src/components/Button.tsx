import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  tone?: 'primary' | 'secondary' | 'ghost';
}

const toneStyles: Record<NonNullable<ButtonProps['tone']>, string> = {
  primary:
    'bg-brand-500 text-white hover:bg-brand-400 focus-visible:outline-brand-300',
  secondary:
    'bg-slate-800 text-slate-100 hover:bg-slate-700 focus-visible:outline-slate-400',
  ghost:
    'bg-transparent text-slate-200 hover:bg-slate-800/60 focus-visible:outline-slate-500',
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
      className={`inline-flex items-center justify-center gap-2 rounded-2xl px-4 py-2 text-sm font-semibold transition focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-60 ${
        toneStyles[tone]
      } ${className}`}
      {...props}
    />
  );
}
