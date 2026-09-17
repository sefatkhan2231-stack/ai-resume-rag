import type { Evidence } from "../types";

interface EvidenceListProps {
  evidence: Evidence[];
}

export default function EvidenceList({ evidence }: EvidenceListProps) {
  if (!evidence.length) {
    return (
      <p className="mt-2 text-sm text-slate-400">
        No supporting evidence found.
      </p>
    );
  }

  return (
    <ul className="mt-3 space-y-3">
      {evidence.map((item, i) => (
        <li key={i} className="rounded-lg border border-slate-200 px-4 py-3">
          <div className="text-xs font-semibold uppercase tracking-wide text-slate-400">
            {item.skill}
          </div>
          <p className="mt-1 text-sm text-slate-700">{item.text}</p>
        </li>
      ))}
    </ul>
  );
}
