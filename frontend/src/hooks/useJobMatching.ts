import { useCallback, useState } from "react";
import { analyzeJobMatching } from "../api/jobMatchingApi";
import type { JobMatchResult } from "../types";

interface UseJobMatchingResult {
  results: JobMatchResult[];
  averageScore: number;
  screeningId: number | null;
  loading: boolean;
  error: string | null;
  runMatching: (
    jobDescription: string,
    candidateIds: string[],
  ) => Promise<void>;
}

export function useJobMatching(): UseJobMatchingResult {
  const [results, setResults] = useState<JobMatchResult[]>([]);
  const [averageScore, setAverageScore] = useState(0);
  const [screeningId, setScreeningId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runMatching = useCallback(
    async (jobDescription: string, candidateIds: string[]) => {
      setLoading(true);
      setError(null);
      try {
        const data = await analyzeJobMatching(jobDescription, candidateIds);
        setResults(data.results);
        setAverageScore(data.average_score);
        setScreeningId(data.screening_id);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Analysis failed.");
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  return { results, averageScore, screeningId, loading, error, runMatching };
}
