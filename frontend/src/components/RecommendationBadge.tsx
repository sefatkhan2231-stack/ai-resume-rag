import type { Recommendation } from "../types";

const STYLES: Record<Recommendation, { icon: string; classes: string }> = {
  "Strong Match": { icon: "●●●", classes: "bg-emerald-100 text-emerald-800" },
  "Good Match": { icon: "●●○", classes: "bg-sky-100 text-sky-800" },
  "Partial Match": { icon: "●○○", classes: "bg-amber-100 text-amber-800" },
  "Weak Match": { icon: "○○○", classes: "bg-red-100 text-red-800" },
};

interface RecommendationBadgeProps {
  recommendation: Recommendation;
}

export default function RecommendationBadge({
  recommendation,
}: RecommendationBadgeProps) {
  const style = STYLES[recommendation];

  return (
    <span
      className={`inline-flex items-center gap-1.5 whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-medium ${style.classes}`}
    >
      <span aria-hidden="true" className="text-[10px] tracking-tighter">
        {style.icon}
      </span>
      {recommendation}
    </span>
  );
}
