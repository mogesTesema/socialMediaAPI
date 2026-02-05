import { useState } from 'react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { api } from '../lib/api';

interface Prediction {
  label: string;
  score_percent: number;
}

type Mode = 'single' | 'batch' | 'zip';

export function FoodVisionPage() {
  const [mode, setMode] = useState<Mode>('single');
  const [file, setFile] = useState<File | null>(null);
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<Prediction[] | null>(null);
  const [batchResults, setBatchResults] = useState<
    { filename: string; prediction: Prediction }[] | null
  >(null);
  const [status, setStatus] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async () => {
    if (mode === 'single' && !file) return;
    if (mode === 'zip' && !file) return;
    if (mode === 'batch' && files.length === 0) return;
    setIsLoading(true);
    setStatus(null);
    setResults(null);
    setBatchResults(null);
    try {
      if (mode === 'single') {
        const response = await api.predictFood(file as File);
        setResults(response.predictions ?? []);
      }
      if (mode === 'batch') {
        const response = await api.predictFoodBatch(files);
        setBatchResults(response.results ?? []);
      }
      if (mode === 'zip') {
        const response = await api.predictFoodZip(file as File);
        setBatchResults(response.results ?? []);
      }
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
        <div className="flex flex-wrap gap-2">
          {([
            { key: 'single', label: 'Single image' },
            { key: 'batch', label: 'Batch images' },
            { key: 'zip', label: 'ZIP of images' },
          ] as const).map((item) => (
            <Button
              key={item.key}
              tone={mode === item.key ? 'primary' : 'secondary'}
              onClick={() => {
                setMode(item.key);
                setFile(null);
                setFiles([]);
                setResults(null);
                setBatchResults(null);
                setStatus(null);
              }}
            >
              {item.label}
            </Button>
          ))}
        </div>
        <p className="text-xs text-slate-400">
          {mode === 'single'
            ? 'Single image returns a ranked list of predictions.'
            : mode === 'batch'
            ? 'Batch images return the top prediction per file (max 32 images).'
            : 'ZIP upload returns the top prediction per image (max 32 images).'}
        </p>
        <div>
          <label className="text-xs uppercase tracking-[0.2em] text-slate-400">
            {mode === 'zip' ? 'ZIP file' : 'Image'}
          </label>
          {mode === 'batch' ? (
            <div className="space-y-3">
              <input
                type="file"
                accept="image/*"
                multiple
                aria-label="Batch image upload"
                className="mt-2 block w-full rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-sm text-slate-100"
                onChange={(event) => {
                  const selected = Array.from(event.target.files ?? []);
                  if (selected.length === 0) return;
                  setFiles((prev) => [...prev, ...selected]);
                  event.currentTarget.value = '';
                }}
              />
              {files.length > 0 && (
                <div className="grid gap-2 rounded-2xl border border-slate-800 bg-slate-950 p-3 text-xs text-slate-300 sm:grid-cols-2 lg:grid-cols-3">
                  {files.map((item, index) => (
                    <div
                      key={`${item.name}-${index}`}
                      className="flex items-center justify-between gap-2 rounded-xl border border-slate-800 bg-slate-900/60 px-3 py-2"
                    >
                      <span className="truncate">{item.name}</span>
                      <button
                        type="button"
                        className="rounded-full border border-rose-500/40 px-2 py-1 text-[10px] font-semibold uppercase tracking-[0.1em] text-rose-200 hover:border-rose-400/70"
                        onClick={() =>
                          setFiles((prev) => prev.filter((_, idx) => idx !== index))
                        }
                      >
                        Remove
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <input
              type="file"
              accept={mode === 'zip' ? '.zip' : 'image/*'}
              aria-label="Single or zip upload"
              className="mt-2 block w-full rounded-2xl border border-slate-800 bg-slate-950 px-4 py-2 text-sm text-slate-100"
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
            />
          )}
        </div>
        <Button
          onClick={handleSubmit}
          disabled={
            isLoading ||
            (mode === 'batch' ? files.length === 0 : file == null)
          }
        >
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
                <p className="text-xs text-slate-400">Score (single image)</p>
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

      {batchResults && (
        <div className="space-y-4">
          <p className="text-xs text-slate-400">
            {mode === 'zip'
              ? 'Top prediction per image inside the zip.'
              : 'Top prediction per uploaded image.'}
          </p>
          {batchResults.map((item) => (
            <Card key={item.filename} className="space-y-2">
              <p className="text-sm font-semibold text-white">{item.filename}</p>
              <p className="text-xs text-slate-400">Top prediction</p>
              <div className="h-2 w-full rounded-full bg-slate-800">
                <div
                  className="h-2 rounded-full bg-brand-500"
                  style={{ width: `${item.prediction.score_percent}%` }}
                />
              </div>
              <p className="text-xs text-slate-300">
                {item.prediction.label} · {item.prediction.score_percent}%
              </p>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
