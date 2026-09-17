interface SkeletonRowsProps {
  rows?: number;
  columns?: number;
}

export default function SkeletonRows({
  rows = 5,
  columns = 6,
}: SkeletonRowsProps) {
  return (
    <>
      {Array.from({ length: rows }).map((_, r) => (
        <tr key={r}>
          {Array.from({ length: columns }).map((_, c) => (
            <td key={c} className="px-4 py-3">
              <div className="h-4 w-full animate-pulse rounded bg-slate-200" />
            </td>
          ))}
        </tr>
      ))}
    </>
  );
}
