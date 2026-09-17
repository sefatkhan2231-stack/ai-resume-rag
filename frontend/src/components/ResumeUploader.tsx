import { useState, type ChangeEvent } from "react";
import { uploadResume, uploadResumes } from "../api/resumeApi";
import type {
  BatchUploadResponse,
  CandidateUploadResult,
  ResumeUploadResponse,
} from "../types";

interface ResumeUploaderProps {
  onUploaded?: (data: ResumeUploadResponse) => void;
  onBatchUploaded?: (data: BatchUploadResponse) => void;
}

export default function ResumeUploader({
  onUploaded,
  onBatchUploaded,
}: ResumeUploaderProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploaded, setUploaded] = useState<ResumeUploadResponse | null>(null);
  const [batchResults, setBatchResults] = useState<
    CandidateUploadResult[] | null
  >(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selected = Array.from(e.target.files ?? []);
    setFiles(selected);
    setError(null);
    setUploaded(null);
    setBatchResults(null);
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setUploading(true);
    setError(null);
    setUploaded(null);
    setBatchResults(null);

    try {
      if (files.length === 1) {
        const data = await uploadResume(files[0]);
        setUploaded(data);
        onUploaded?.(data);
      } else {
        const data = await uploadResumes(files);
        setBatchResults(data.uploaded);
        onBatchUploaded?.(data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const successCount = batchResults?.filter((r) => r.success).length ?? 0;

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-800">
        1. Upload Resumes
      </h2>
      <p className="mt-1 text-sm text-slate-500">
        PDF only. Select multiple files to batch upload.
      </p>

      <div className="mt-4 flex items-center gap-3">
        <input
          type="file"
          accept="application/pdf"
          multiple
          onChange={handleFileChange}
          className="block w-full text-sm text-slate-600 file:mr-4 file:rounded-lg file:border-0 file:bg-slate-100 file:px-4 file:py-2 file:text-sm file:font-medium file:text-slate-700 hover:file:bg-slate-200"
        />
        <button
          onClick={handleUpload}
          disabled={files.length === 0 || uploading}
          className="shrink-0 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
        >
          {uploading
            ? "Uploading…"
            : files.length > 1
              ? `Upload ${files.length} files`
              : "Upload"}
        </button>
      </div>

      {files.length > 0 && (
        <p className="mt-2 text-xs text-slate-500">
          {files.length === 1
            ? files[0].name
            : `${files.length} files selected: ${files
                .map((f) => f.name)
                .join(", ")}`}
        </p>
      )}

      {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

      {uploaded && (
        <div className="mt-4 rounded-lg bg-emerald-50 px-4 py-3 text-sm text-emerald-800">
          Indexed <strong>{uploaded.filename}</strong> —{" "}
          {uploaded.chunks_indexed} chunks embedded.
        </div>
      )}

      {batchResults && (
        <div className="mt-4 space-y-2">
          <p className="text-sm font-medium text-slate-700">
            {successCount} of {batchResults.length} uploaded successfully
          </p>
          <ul className="space-y-1.5">
            {batchResults.map((result, i) => (
              <li
                key={`${result.filename}-${i}`}
                className={`rounded-lg px-4 py-2 text-sm ${
                  result.success
                    ? "bg-emerald-50 text-emerald-800"
                    : "bg-red-50 text-red-700"
                }`}
              >
                <strong>{result.filename}</strong>
                {result.success ? (
                  <span> — {result.chunks_indexed} chunks embedded.</span>
                ) : (
                  <span> — {result.error}</span>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
