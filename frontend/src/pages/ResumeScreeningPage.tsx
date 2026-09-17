import { useMemo, useState } from "react";
import CandidateDrawer from "../components/CandidateDrawer";
import ErrorState from "../components/ErrorState";
import ExportCsvButton from "../components/ExportCsvButton";
import MultiFileDropzone, {
  type PendingFile,
} from "../components/MultiFileDropzone";
import RecommendationBadge from "../components/RecommendationBadge";
import ResultsTable, { type Column } from "../components/ResultsTable";
import ScoreBadge from "../components/ScoreBadge";
import { useToast } from "../context/ToastContext";
import { useBatchUpload } from "../hooks/useBatchUpload";
import { useRanking } from "../hooks/useRanking";
import type { RankedCandidate } from "../types";

export default function ResumeScreeningPage() {
  const [pendingFiles, setPendingFiles] = useState<PendingFile[]>([]);
  const [jobDescription, setJobDescription] = useState("");
  const [selectedCandidate, setSelectedCandidate] =
    useState<RankedCandidate | null>(null);

  const {
    results: uploadResults,
    uploading,
    error: uploadError,
    upload,
  } = useBatchUpload();
  const {
    results,
    averageScore,
    screeningId,
    loading,
    error: rankError,
    runRanking,
  } = useRanking();
  const { addToast } = useToast();

  const uploadedCandidateIds = useMemo(
    () =>
      uploadResults
        .filter((r) => r.success)
        .map((r) => r.candidate_id!)
        .filter(Boolean),
    [uploadResults],
  );

  const handleProcess = async () => {
    if (!pendingFiles.length) return;
    const outcomes = await upload(pendingFiles.map((p) => p.file));
    const failed = outcomes.filter((o) => !o.success);
    if (failed.length) {
      addToast(`${failed.length} file(s) failed to process.`, "error");
    } else {
      addToast(
        `${outcomes.length} resume(s) processed successfully.`,
        "success",
      );
    }
  };

  const handleRank = async () => {
    if (!jobDescription.trim() || !uploadedCandidateIds.length) return;
    await runRanking(jobDescription, uploadedCandidateIds);
  };

  const columns: Column<RankedCandidate>[] = [
    {
      key: "rank",
      header: "Rank",
      render: (r) => `#${r.rank}`,
      sortValue: (r) => r.rank,
    },
    {
      key: "name",
      header: "Candidate",
      render: (r) => r.name,
      sortValue: (r) => r.name,
    },
    { key: "email", header: "Email", render: (r) => r.email || "—" },
    {
      key: "skills",
      header: "Skills",
      render: (r) => (
        <span className="text-xs text-slate-500">
          {r.matched_skills.length} matched / {r.missing_skills.length} missing
        </span>
      ),
    },
    {
      key: "score",
      header: "Match Score",
      render: (r) => <ScoreBadge score={r.score} />,
      sortValue: (r) => r.score,
    },
    {
      key: "recommendation",
      header: "Status",
      render: (r) => <RecommendationBadge recommendation={r.recommendation} />,
    },
    {
      key: "actions",
      header: "Actions",
      render: (r) => (
        <button
          onClick={(e) => {
            e.stopPropagation();
            setSelectedCandidate(r);
          }}
          className="text-xs font-medium text-slate-600 underline hover:text-slate-900"
        >
          View
        </button>
      ),
    },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900">Resume Screening</h1>
      <p className="mt-1 text-sm text-slate-500">
        Upload multiple resumes and rank them against a job description.
      </p>

      <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-800">
          1. Upload Resumes
        </h2>
        <div className="mt-3">
          <MultiFileDropzone
            files={pendingFiles}
            onFilesChange={setPendingFiles}
            disabled={uploading}
          />
        </div>
        <button
          onClick={handleProcess}
          disabled={!pendingFiles.length || uploading}
          className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
        >
          {uploading
            ? "Processing…"
            : `Process ${pendingFiles.length || ""} Resume(s)`}
        </button>

        {uploadError && (
          <div className="mt-3">
            <ErrorState message={uploadError} />
          </div>
        )}

        {uploadResults.length > 0 && (
          <ul className="mt-4 space-y-1 text-sm">
            {uploadResults.map((r) => (
              <li
                key={r.filename}
                className={r.success ? "text-emerald-700" : "text-red-600"}
              >
                {r.success ? "✓" : "✗"} {r.filename}
                {!r.success && r.error && ` — ${r.error}`}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="text-sm font-semibold text-slate-800">
          2. Job Description
        </h2>
        <textarea
          rows={6}
          placeholder="Paste the job description here…"
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="mt-3 w-full resize-y rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
        />
        <button
          onClick={handleRank}
          disabled={
            !jobDescription.trim() || !uploadedCandidateIds.length || loading
          }
          className="mt-3 rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
        >
          {loading ? "Ranking…" : "Rank Candidates"}
        </button>
        {!uploadedCandidateIds.length && (
          <p className="mt-2 text-xs text-slate-400">
            Process at least one resume first.
          </p>
        )}
      </div>

      {rankError && (
        <div className="mt-6">
          <ErrorState message={rankError} />
        </div>
      )}

      {(results.length > 0 || loading) && (
        <div className="mt-6">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-sm text-slate-600">
              {results.length > 0 && `Average match score: ${averageScore}%`}
            </p>
            <ExportCsvButton screeningId={screeningId} />
          </div>
          <ResultsTable
            rows={results}
            columns={columns}
            rowKey={(r) => r.candidate_id}
            loading={loading}
            searchPlaceholder="Search candidates…"
            searchFilter={(r, q) =>
              r.name.toLowerCase().includes(q) ||
              (r.email || "").toLowerCase().includes(q)
            }
            emptyTitle="No candidates match your search"
          />
        </div>
      )}

      <CandidateDrawer
        candidate={selectedCandidate}
        onClose={() => setSelectedCandidate(null)}
      />
    </div>
  );
}
