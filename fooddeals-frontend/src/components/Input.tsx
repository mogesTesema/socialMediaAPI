import { InputHTMLAttributes } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
}

export function Input({ label, className = '', ...props }: InputProps) {
  return (
    <label className="flex flex-col gap-2 text-sm text-slate-200">
      {label && <span className="text-xs uppercase tracking-[0.2em] text-slate-400">{label}</span>}
      <input
        className={`rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus:border-brand-400 focus:outline-none ${className}`}
        {...props}
      />
    </label>
  );
}
