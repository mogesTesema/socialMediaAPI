import { Input } from '../../components/Input';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <div className="rounded-3xl border border-cyan-400/30 bg-cyan-500/5 p-4">
      <Input
        label="Search posts"
        placeholder="Search by dish, deal, or ingredient..."
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
      <p className="mt-2 text-xs text-amber-200/60">
        This is a client-side search. Later you can swap in a server-side search endpoint.
      </p>
    </div>
  );
}
