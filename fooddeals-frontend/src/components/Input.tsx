import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({ label, className = '', ...props }: InputProps) {
  return (
    <label className="flex flex-col gap-2 text-sm text-slate-200">
      {label && (
        <span className="text-xs uppercase tracking-[0.2em] text-amber-200/70">
          {label}
        </span>
      )}
      <input
        className={`rounded-2xl border border-sky-500/30 bg-emerald-500/10 px-4 py-2 text-sm text-slate-100 placeholder:text-amber-200/40 focus:border-brand-400 focus:outline-none ${className}`}
        {...props}
      />
    </label>
  );
}
