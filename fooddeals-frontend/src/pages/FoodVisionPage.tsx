import { useState } from 'react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { api } from '../lib/api';

interface Prediction {
  label: string;
  score_percent: number;
}

export function FoodVisionPage() {
  const [file, setFile] = useState<File | null>(null);
  const [results, setResults] = useState<Prediction[] | null>(null);
  const [status, setStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (!file) return;
    setIsLoading(true);
    setStatus(null);
    setResults(null);
    try {
      const response = await api.predictFood(file);
      setResults(response.predictions ?? []);
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Prediction failed';
      setStatus(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-semibold text-white">Food vision lab</h2>
        <p className="text-sm text-slate-400">
          Upload a food image and get classification results from the ONNX model.
        </p>
      </div>

      <Card className="space-y-4">
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-slate-400">Image</label>
          <input
            type="file"
            accept="image/*"
            className="mt-2 block w-full rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-sm text-slate-100"
            onChange={(event) => setFile(event.target.files?.[0] ?? null)}
          />
        </div>
        <Button onClick={handleSubmit} disabled={!file || isLoading}>
          {isLoading ? 'Predicting...' : 'Run prediction'}
        </Button>
        {status && (
          <div className="rounded-2xl border border-rose-500/40 bg-rose-500/10 px-4 py-2 text-xs text-rose-200">
            {status}
          </div>
        )}
      </Card>

      {results && (
        <div className="grid gap-4 md:grid-cols-2">
          {results.length === 0 ? (
            <Card>No predictions returned.</Card>
          ) : (
            results.map((item) => (
              <Card key={item.label} className="space-y-2">
                <p className="text-sm font-semibold text-white">{item.label}</p>
                <p className="text-xs text-slate-400">Score</p>
                <div className="h-2 w-full rounded-full bg-slate-800">
                  <div
                    className="h-2 rounded-full bg-brand-500"
                    style={{ width: `${item.score_percent}%` }}
                  />
                </div>
                <p className="text-xs text-slate-300">{item.score_percent}%</p>
              </Card>
            ))
          )}
        </div>
      )}
    </div>
  );
}
