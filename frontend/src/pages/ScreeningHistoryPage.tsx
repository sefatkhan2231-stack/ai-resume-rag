import { useEffect, useState } from "react";
import { getScreeningHistory } from "../api/dashboardApi";
import ErrorState from "../components/ErrorState";
import ExportCsvButton from "../components/ExportCsvButton";
import ResultsTable, { type Column } from "../components/ResultsTable";
import type { ScreeningHistoryItem } from "../types";

const TYPE_LABEL: Record<ScreeningHistoryItem["screening_type"], string> = {
  resume_ranking: "Resume Screening",
  job_matching: "Job Matching",
};

export default function ScreeningHistoryPage() {
  const [history, setHistory] = useState<ScreeningHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await getScreeningHistory(100);
        if (!cancelled) setHistory(data);
      } catch (err) {
        if (!cancelled)
          setError(
            err instanceof Error ? err.message : "Failed to load history.",
          );
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const columns: Column<ScreeningHistoryItem>[] = [
    {
      key: "created_at",
      header: "Date",
      render: (r) => new Date(r.created_at).toLocaleString(),
      sortValue: (r) => r.created_at,
    },
    {
      key: "screening_type",
      header: "Type",
      render: (r) => TYPE_LABEL[r.screening_type],
      sortValue: (r) => r.screening_type,
    },
    {
      key: "number_of_resumes",
      header: "Resumes",
      render: (r) => r.number_of_resumes,
      sortValue: (r) => r.number_of_resumes,
    },
    {
      key: "average_score",
      header: "Avg Score",
      render: (r) => `${r.average_score}%`,
      sortValue: (r) => r.average_score,
    },
    {
      key: "export",
      header: "Export",
      render: (r) => <ExportCsvButton screeningId={r.id} />,
    },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900">Screening History</h1>
      <p className="mt-1 text-sm text-slate-500">
        Past ranking and job-matching runs.
      </p>

      {error && (
        <div className="mt-6">
          <ErrorState message={error} />
        </div>
      )}

      {!error && (
        <div className="mt-6">
          <ResultsTable
            rows={history}
            columns={columns}
            rowKey={(r) => String(r.id)}
            loading={loading}
            searchPlaceholder="Search by type…"
            searchFilter={(r, q) =>
              TYPE_LABEL[r.screening_type].toLowerCase().includes(q)
            }
            emptyTitle="No screenings yet"
            emptyDescription="Run a resume screening or job matching pass to see it here."
          />
        </div>
      )}
    </div>
  );
}
