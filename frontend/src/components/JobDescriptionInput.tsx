import { useState } from "react";

interface JobDescriptionInputProps {
  onSubmit: (jobDescription: string, candidateName: string) => void;
  loading: boolean;
  disabled: boolean;
  defaultCandidateName?: string;
}

export default function JobDescriptionInput({
  onSubmit,
  loading,
  disabled,
  defaultCandidateName,
}: JobDescriptionInputProps) {
  const [jobDescription, setJobDescription] = useState("");
  const [candidateName, setCandidateName] = useState(
    defaultCandidateName ?? "",
  );

  const handleSubmit = () => {
    if (!jobDescription.trim()) return;
    onSubmit(jobDescription, candidateName || "Candidate");
  };

  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-slate-800">
        2. Job Description
      </h2>

      <input
        type="text"
        placeholder="Candidate name (optional)"
        value={candidateName}
        onChange={(e) => setCandidateName(e.target.value)}
        className="mt-4 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
      />

      <textarea
        rows={8}
        placeholder="Paste the job description here…"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        className="mt-3 w-full resize-y rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
      />

      <button
        onClick={handleSubmit}
        disabled={disabled || loading || !jobDescription.trim()}
        className="mt-4 w-full rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-40"
      >
        {loading ? "Screening…" : "Screen Candidate"}
      </button>

      {disabled && (
        <p className="mt-2 text-xs text-slate-400">Upload a resume first.</p>
      )}
    </div>
  );
}
