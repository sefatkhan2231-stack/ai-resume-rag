import { useCallback, useRef, useState, type DragEvent } from "react";

export interface PendingFile {
  file: File;
  id: string;
}

interface MultiFileDropzoneProps {
  files: PendingFile[];
  onFilesChange: (files: PendingFile[]) => void;
  disabled?: boolean;
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function MultiFileDropzone({
  files,
  onFilesChange,
  disabled,
}: MultiFileDropzoneProps) {
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const addFiles = useCallback(
    (incoming: FileList | null) => {
      if (!incoming) return;
      const pdfsOnly: PendingFile[] = Array.from(incoming)
        .filter((f) => f.type === "application/pdf")
        .map((f) => ({ file: f, id: `${f.name}-${f.size}-${f.lastModified}` }));

      const existingIds = new Set(files.map((f) => f.id));
      const deduped = pdfsOnly.filter((f) => !existingIds.has(f.id));

      onFilesChange([...files, ...deduped]);
    },
    [files, onFilesChange],
  );

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setDragActive(false);
    if (disabled) return;
    addFiles(e.dataTransfer.files);
  };

  const removeFile = (id: string) => {
    onFilesChange(files.filter((f) => f.id !== id));
  };

  return (
    <div>
      <div
        onDragOver={(e) => {
          e.preventDefault();
          if (!disabled) setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors ${
          dragActive
            ? "border-slate-500 bg-slate-50"
            : "border-slate-300 bg-white"
        } ${disabled ? "cursor-not-allowed opacity-50" : "hover:border-slate-400"}`}
      >
        <p className="text-sm font-medium text-slate-700">
          Drag and drop resumes here, or click to browse
        </p>
        <p className="mt-1 text-xs text-slate-400">
          PDF only, multiple files supported
        </p>
        <input
          ref={inputRef}
          type="file"
          accept="application/pdf"
          multiple
          disabled={disabled}
          onChange={(e) => addFiles(e.target.files)}
          className="hidden"
        />
      </div>

      {files.length > 0 && (
        <ul className="mt-4 divide-y divide-slate-100 rounded-xl border border-slate-200 bg-white">
          {files.map(({ file, id }) => (
            <li
              key={id}
              className="flex items-center justify-between px-4 py-2.5 text-sm"
            >
              <div className="min-w-0">
                <p className="truncate font-medium text-slate-700">
                  {file.name}
                </p>
                <p className="text-xs text-slate-400">
                  {formatSize(file.size)}
                </p>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  removeFile(id);
                }}
                disabled={disabled}
                className="ml-3 shrink-0 text-xs font-medium text-red-600 hover:text-red-700 disabled:opacity-40"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
