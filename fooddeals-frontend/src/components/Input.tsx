import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({ label, className = '', ...props }: InputProps) {
  return (
    <label className="flex flex-col gap-2 text-sm text-slate-200">
      {label && (
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">
          {label}
        </span>
      )}
      <input
        className={`rounded-2xl border border-slate-600/50 bg-slate-800/40 px-4 py-3 text-sm text-slate-100 placeholder:text-slate-500 focus:border-primary-500/70 focus:outline-none focus:ring-2 focus:ring-primary-500/30 transition-all duration-200 backdrop-blur-sm ${className}`}
        {...props}
      />
    </label>
  );
}
