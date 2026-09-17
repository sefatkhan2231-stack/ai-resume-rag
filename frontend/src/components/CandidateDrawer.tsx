import type { JobMatchResult, RankedCandidate } from "../types";
import EvidenceList from "./EvidenceList";
import RecommendationBadge from "./RecommendationBadge";
import ScoreBadge from "./ScoreBadge";
import SkillList from "./SkillList";

type DrawerCandidate = RankedCandidate | JobMatchResult;

function hasFullAssessment(c: DrawerCandidate): c is JobMatchResult {
  return "overall_assessment" in c;
}

interface CandidateDrawerProps {
  candidate: DrawerCandidate | null;
  onClose: () => void;
}

export default function CandidateDrawer({
  candidate,
  onClose,
}: CandidateDrawerProps) {
  if (!candidate) return null;

  const skills: Record<string, boolean> = {
    ...Object.fromEntries(candidate.matched_skills.map((s) => [s, true])),
    ...Object.fromEntries(candidate.missing_skills.map((s) => [s, false])),
  };

  return (
    <div className="fixed inset-0 z-40 flex justify-end">
      <div className="absolute inset-0 bg-slate-900/30" onClick={onClose} />

      <div className="relative flex h-full w-full max-w-lg flex-col overflow-y-auto bg-white p-6 shadow-xl">
        <div className="flex items-start justify-between">
          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              {candidate.name}
            </h2>
            {candidate.email && (
              <p className="text-sm text-slate-500">{candidate.email}</p>
            )}
            {candidate.phone && (
              <p className="text-sm text-slate-500">{candidate.phone}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="rounded-lg px-2 py-1 text-slate-400 hover:bg-slate-100 hover:text-slate-600"
            aria-label="Close"
          >
            ✕
          </button>
        </div>

        <div className="mt-4 flex items-center gap-3">
          <ScoreBadge score={candidate.score} />
          <RecommendationBadge recommendation={candidate.recommendation} />
        </div>

        {hasFullAssessment(candidate) && candidate.overall_assessment && (
          <div className="mt-5">
            <h3 className="text-sm font-semibold text-slate-800">
              Overall Assessment
            </h3>
            <p className="mt-1 text-sm text-slate-700">
              {candidate.overall_assessment}
            </p>
          </div>
        )}

        <div className="mt-5">
          <h3 className="text-sm font-semibold text-slate-800">Skills</h3>
          <SkillList skills={skills} />
        </div>

        {hasFullAssessment(candidate) && (
          <>
            {candidate.evidence.length > 0 && (
              <div className="mt-5">
                <h3 className="text-sm font-semibold text-slate-800">
                  Resume Evidence
                </h3>
                <EvidenceList evidence={candidate.evidence} />
              </div>
            )}

            {candidate.final_recommendation && (
              <div className="mt-5">
                <h3 className="text-sm font-semibold text-slate-800">
                  Recommendation
                </h3>
                <p className="mt-1 text-sm text-slate-700">
                  {candidate.final_recommendation}
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
