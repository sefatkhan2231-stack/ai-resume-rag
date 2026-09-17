interface EmptyStateProps {
  title: string;
  description?: string;
}

export default function EmptyState({ title, description }: EmptyStateProps) {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center">
      <p className="text-sm font-medium text-slate-700">{title}</p>
      {description && (
        <p className="mt-1 text-sm text-slate-400">{description}</p>
      )}
    </div>
  );
}
