import { Input } from '../../components/Input';
import { Card } from '../../components/Card';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

export function SearchBar({ value, onChange }: SearchBarProps) {
  return (
    <Card variant="cyan" className="space-y-3">
      <div className="flex items-center gap-2">
        <span className="text-2xl">🔍</span>
        <h3 className="font-bold text-accent-cyan/90">Search Posts</h3>
      </div>
      <Input
        label=""
        placeholder="Search by dish, deal, or ingredient..."
        value={value}
        onChange={(event) => onChange(event.target.value)}
      />
      <p className="text-xs text-slate-400 italic border-t border-accent-cyan/30 pt-3">
        💡 Client-side search filters posts instantly as you type
      </p>
    </Card>
  );
}
