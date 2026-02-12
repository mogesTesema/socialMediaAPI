import { useState, useRef, ChangeEvent } from 'react';
import { Button } from './Button';

interface FileUploaderProps {
  onFileSelect: (file: File) => void;
  accept?: string;
  label?: string;
  disabled?: boolean;
}

export function FileUploader({
  onFileSelect,
  accept = 'image/*',
  label = 'Upload File',
  disabled = false,
}: FileUploaderProps) {
  const [fileName, setFileName] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setFileName(file.name);
      onFileSelect(file);
    }
  };

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleClear = () => {
    setFileName(null);
    if (inputRef.current) {
      inputRef.current.value = '';
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <input
        type="file"
        ref={inputRef}
        onChange={handleFileChange}
        accept={accept}
        className="hidden"
        disabled={disabled}
      />
      <div className="flex items-center gap-2">
        <Button
          onClick={handleClick}
          type="button"
          tone="secondary"
          disabled={disabled}
        >
          {label}
        </Button>
        {fileName && (
          <div className="flex items-center gap-2 rounded-lg border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-xs text-sky-200">
            <span className="max-w-[150px] truncate">{fileName}</span>
            <button
              onClick={handleClear}
              className="text-sky-200/50 hover:text-white"
              title="Remove file"
            >
              ✕
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
