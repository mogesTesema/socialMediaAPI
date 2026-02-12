import { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  tone?: 'primary' | 'secondary' | 'ghost' | 'emerald' | 'purple' | 'pink' | 'orange' | 'cyan';
}

const toneStyles: Record<NonNullable<ButtonProps['tone']>, string> = {
  primary:
    'bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-[0_16px_34px_-18px_rgba(59,130,246,0.7)] hover:from-primary-400 hover:to-primary-500 active:from-primary-600 active:to-primary-700 focus-visible:outline-primary-300',
  secondary:
    'border border-primary-500/50 bg-primary-500/10 text-primary-100 hover:bg-primary-500/20 hover:border-primary-400 active:bg-primary-500/30 focus-visible:outline-primary-300 backdrop-blur-sm',
  ghost:
    'border border-slate-600/50 bg-slate-700/20 text-slate-100 hover:bg-slate-700/40 active:bg-slate-700/60 focus-visible:outline-slate-400 backdrop-blur-sm',
  emerald:
    'border border-accent-emerald/50 bg-accent-emerald/10 text-accent-emerald/90 hover:bg-accent-emerald/20 active:bg-accent-emerald/30 focus-visible:outline-accent-emerald/50',
  purple:
    'border border-accent-purple/50 bg-accent-purple/10 text-accent-purple/90 hover:bg-accent-purple/20 active:bg-accent-purple/30 focus-visible:outline-accent-purple/50',
  pink:
    'border border-accent-pink/50 bg-accent-pink/10 text-accent-pink/90 hover:bg-accent-pink/20 active:bg-accent-pink/30 focus-visible:outline-accent-pink/50',
  orange:
    'border border-accent-orange/50 bg-accent-orange/10 text-accent-orange/90 hover:bg-accent-orange/20 active:bg-accent-orange/30 focus-visible:outline-accent-orange/50',
  cyan:
    'border border-accent-cyan/50 bg-accent-cyan/10 text-accent-cyan/90 hover:bg-accent-cyan/20 active:bg-accent-cyan/30 focus-visible:outline-accent-cyan/50',
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
      className={`inline-flex min-h-11 items-center justify-center gap-2 rounded-2xl px-5 py-3 text-base font-semibold transition-all duration-200 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 disabled:cursor-not-allowed disabled:opacity-50 disabled:pointer-events-none ${
        toneStyles[tone]
      } ${className}`}
      {...props}
    />
  );
}
