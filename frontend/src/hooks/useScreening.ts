import { useCallback, useState } from "react";
import { screenCandidate } from "../api/screeningApi";
import type { ScreeningResponse } from "../types";

interface UseScreeningResult {
  result: ScreeningResponse | null;
  loading: boolean;
  error: string | null;
  runScreening: (
    jobDescription: string,
    candidateId: string,
    candidateName?: string,
  ) => Promise<ScreeningResponse | null>;
  reset: () => void;
}

export function useScreening(): UseScreeningResult {
  const [result, setResult] = useState<ScreeningResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runScreening = useCallback(
    async (
      jobDescription: string,
      candidateId: string,
      candidateName?: string,
    ) => {
      setLoading(true);
      setError(null);

      try {
        const data = await screenCandidate(
          jobDescription,
          candidateId,
          candidateName,
        );
        setResult(data);
        return data;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Screening failed.");
        return null;
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  const reset = useCallback(() => {
    setResult(null);
    setError(null);
  }, []);

  return { result, loading, error, runScreening, reset };
}
