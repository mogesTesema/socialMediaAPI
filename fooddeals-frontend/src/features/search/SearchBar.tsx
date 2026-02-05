import { Input } from '../../components/Input';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-4">
      <Input
        label="Search posts"
        placeholder="Search by dish, deal, or ingredient..."
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
      <p className="mt-2 text-xs text-slate-500">
        This is a client-side search. Later you can swap in a server-side search endpoint.
      </p>
    </div>
  );
}
