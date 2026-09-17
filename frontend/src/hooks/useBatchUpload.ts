import { useCallback, useState } from "react";
import { uploadResumes } from "../api/resumeApi";
import type { CandidateUploadResult } from "../types";

interface UseBatchUploadResult {
  results: CandidateUploadResult[];
  uploading: boolean;
  error: string | null;
  upload: (files: File[]) => Promise<CandidateUploadResult[]>;
  reset: () => void;
}

export function useBatchUpload(): UseBatchUploadResult {
  const [results, setResults] = useState<CandidateUploadResult[]>([]);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const upload = useCallback(async (files: File[]) => {
    setUploading(true);
    setError(null);
    try {
      const response = await uploadResumes(files);
      setResults(response.uploaded);
      return response.uploaded;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
      return [];
    } finally {
      setUploading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setResults([]);
    setError(null);
  }, []);

  return { results, uploading, error, upload, reset };
}
