import { useState } from 'react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { api } from '../lib/api';
import { FileUploader } from '../components/FileUploader';

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
  const [statusTone, setStatusTone] = useState<'success' | 'error' | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Helper for multi-file input
  const handleBatchSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  const handleSubmit = async () => {
    if (mode === 'single' && !file) return;
    if (mode === 'zip' && !file) return;
    if (mode === 'batch' && files.length === 0) return;
    setIsLoading(true);
    setStatus(null);
    setStatusTone(null);
    setResults(null);
    setBatchResults(null);
    try {
      if (mode === 'single') {
        const response = await api.predictFood(file as File);
        setResults(response.predictions ?? []);
        setStatus('Prediction complete.');
        setStatusTone('success');
      }
      if (mode === 'batch') {
        const response = await api.predictFoodBatch(files);
        setBatchResults(response.results ?? []);
        setStatus('Batch predictions complete.');
        setStatusTone('success');
      }
      if (mode === 'zip') {
        const response = await api.predictFoodZip(file as File);
        setBatchResults(response.results ?? []);
        setStatus('ZIP predictions complete.');
        setStatusTone('success');
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Prediction failed';
      setStatus(message);
      setStatusTone('error');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-semibold text-white">Food vision lab</h2>
        <p className="text-sm text-amber-200/70">
          Upload a food image and get classification results from the ONNX model.
        </p>
      </div>

      <Card className="space-y-4 border-sky-500/30 bg-sky-500/5">
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
                setStatusTone(null);
              }}
            >
              {item.label}
            </Button>
          ))}
        </div>
        <p className="text-xs text-amber-200/70">
          {mode === 'single'
            ? 'Single image returns a ranked list of predictions.'
            : mode === 'batch'
            ? 'Batch images return the top prediction per file (max 32 images).'
            : 'ZIP upload returns the top prediction per image (max 32 images).'}
        </p>

        <div className="flex flex-col gap-4">
           {mode === 'single' && (
              <FileUploader onFileSelect={setFile} label="Select Image" />
           )}
           {mode === 'zip' && (
              <FileUploader onFileSelect={setFile} label="Select ZIP" accept=".zip,application/zip" />
           )}
           {mode === 'batch' && (
             <div className="flex flex-col gap-2">
               <input
                 type="file"
                 multiple
                 accept="image/*"
                 onChange={handleBatchSelect}
                 className="block w-full text-sm text-slate-300 file:mr-4 file:rounded-full file:border-0 file:bg-sky-500/20 file:px-4 file:py-2 file:text-sm file:font-semibold file:text-sky-200 hover:file:bg-sky-500/30"
               />
               <div className="text-xs text-slate-400">
                  {files.length} file{files.length !== 1 ? 's' : ''} selected
               </div>
             </div>
           )}

           <Button onClick={handleSubmit} disabled={isLoading || (mode === 'batch' ? files.length === 0 : !file)}>
              {isLoading ? 'Processing...' : 'Run Prediction'}
           </Button>
        </div>

        {status && (
           <div
             className={`rounded-2xl border px-4 py-2 text-xs ${
               statusTone === 'success'
                 ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-200'
                 : 'border-rose-500/40 bg-rose-500/10 text-rose-200'
             }`}
           >
             {status}
           </div>
        )}
      </Card>

      {/* Results Display */}
      {results && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
           <Card className="border-emerald-500/30 bg-emerald-500/5">
              <h4 className="mb-2 font-semibold text-white">Top Prediction</h4>
              <div className="text-2xl text-emerald-300 text-center py-4">
                 {results[0]?.label}
              </div>
              <div className="text-center text-sm text-emerald-200/60">
                 {results[0]?.score_percent.toFixed(1)}% confidence
              </div>
           </Card>
           
           <Card className="sm:col-span-2 lg:col-span-2">
              <h4 className="mb-4 font-semibold text-white">All Candidates</h4>
              <div className="space-y-2">
                 {results.map((pred, i) => (
                    <div key={pred.label} className="flex items-center gap-2 text-sm">
                       <span className="w-6 text-slate-500">#{i + 1}</span>
                       <span className="flex-1 text-slate-200">{pred.label}</span>
                       <div className="w-32 h-2 bg-slate-700 rounded-full overflow-hidden">
                          <div className="h-full bg-sky-500" style={{ width: `${pred.score_percent}%` }} />
                       </div>
                       <span className="w-12 text-right text-slate-400">{Math.round(pred.score_percent)}%</span>
                    </div>
                 ))}
              </div>
           </Card>
        </div>
      )}

      {batchResults && (
         <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {batchResults.map((res, i) => (
               <Card key={i} className="border-sky-500/20 bg-sky-500/5">
                  <div className="text-xs text-sky-200/50 truncate mb-1" title={res.filename}>{res.filename}</div>
                  <div className="text-lg font-medium text-sky-100">{res.prediction.label}</div>
                  <div className="text-xs text-sky-200/60">{res.prediction.score_percent}% confidence</div>
               </Card>
            ))}
         </div>
      )}
    </div>

  );
}
