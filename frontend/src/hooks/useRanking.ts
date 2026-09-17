import { useCallback, useState } from "react";
import { rankCandidates } from "../api/resumeApi";
import type { RankedCandidate } from "../types";

interface UseRankingResult {
  results: RankedCandidate[];
  averageScore: number;
  screeningId: number | null;
  loading: boolean;
  error: string | null;
  runRanking: (jobDescription: string, candidateIds: string[]) => Promise<void>;
}

export function useRanking(): UseRankingResult {
  const [results, setResults] = useState<RankedCandidate[]>([]);
  const [averageScore, setAverageScore] = useState(0);
  const [screeningId, setScreeningId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runRanking = useCallback(
    async (jobDescription: string, candidateIds: string[]) => {
      setLoading(true);
      setError(null);
      try {
        const data = await rankCandidates(jobDescription, candidateIds);
        setResults(data.results);
        setAverageScore(data.average_score);
        setScreeningId(data.screening_ids);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Ranking failed.");
      } finally {
        setLoading(false);
      }
    },
    [],
  );

  return { results, averageScore, screeningId, loading, error, runRanking };
}
