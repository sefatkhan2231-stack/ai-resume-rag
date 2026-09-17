interface ScoreBadgeProps {
  score: number;
}

export default function ScoreBadge({ score }: ScoreBadgeProps) {
  const color =
    score >= 75
      ? "bg-emerald-100 text-emerald-800"
      : score >= 40
        ? "bg-amber-100 text-amber-800"
        : "bg-red-100 text-red-800";

  return (
    <div
      className={`inline-flex items-center rounded-full px-4 py-1.5 text-2xl font-bold ${color}`}
    >
      {score.toFixed(0)}%
    </div>
  );
}
