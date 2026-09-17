interface LoadingStateProps {
  label?: string;
}

export default function LoadingState({
  label = "Loading…",
}: LoadingStateProps) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-6 text-sm text-slate-500 shadow-sm">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-slate-700" />
      {label}
    </div>
  );
}
