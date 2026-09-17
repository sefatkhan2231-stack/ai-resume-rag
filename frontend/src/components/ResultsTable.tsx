import { useMemo, useState, type ReactNode } from "react";
import EmptyState from "./EmptyState";
import SkeletonRows from "./SkeletonRows";

export interface Column<T> {
  key: string;
  header: string;
  render: (row: T) => ReactNode;
  sortValue?: (row: T) => number | string;
}

interface ResultsTableProps<T> {
  rows: T[];
  columns: Column<T>[];
  rowKey: (row: T) => string;
  searchFilter: (row: T, query: string) => boolean;
  searchPlaceholder?: string;
  onRowClick?: (row: T) => void;
  loading?: boolean;
  emptyTitle?: string;
  emptyDescription?: string;
  pageSize?: number;
}

type SortDirection = "asc" | "desc";

export default function ResultsTable<T>({
  rows,
  columns,
  rowKey,
  searchFilter,
  searchPlaceholder = "Search…",
  onRowClick,
  loading = false,
  emptyTitle = "No results yet",
  emptyDescription,
  pageSize = 10,
}: ResultsTableProps<T>) {
  const [query, setQuery] = useState("");
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<SortDirection>("desc");
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    if (!query.trim()) return rows;
    return rows.filter((row) => searchFilter(row, query.trim().toLowerCase()));
  }, [rows, query, searchFilter]);

  const sorted = useMemo(() => {
    if (!sortKey) return filtered;
    const column = columns.find((c) => c.key === sortKey);
    if (!column?.sortValue) return filtered;

    const copy = [...filtered];
    copy.sort((a, b) => {
      const av = column.sortValue!(a);
      const bv = column.sortValue!(b);
      const cmp =
        typeof av === "number" && typeof bv === "number"
          ? av - bv
          : String(av).localeCompare(String(bv));
      return sortDir === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [filtered, sortKey, sortDir, columns]);

  const totalPages = Math.max(1, Math.ceil(sorted.length / pageSize));
  const currentPage = Math.min(page, totalPages);
  const paginated = sorted.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize,
  );

  const toggleSort = (column: Column<T>) => {
    if (!column.sortValue) return;
    if (sortKey === column.key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(column.key);
      setSortDir("desc");
    }
    setPage(1);
  };

  return (
    <div>
      <input
        type="text"
        placeholder={searchPlaceholder}
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setPage(1);
        }}
        className="mb-3 w-full max-w-xs rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-slate-500 focus:outline-none"
      />

      <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
        <table className="w-full min-w-max text-left text-sm">
          <thead className="border-b border-slate-200 bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th
                  key={column.key}
                  onClick={() => toggleSort(column)}
                  className={`whitespace-nowrap px-4 py-3 text-xs font-semibold uppercase tracking-wide text-slate-500 ${
                    column.sortValue
                      ? "cursor-pointer select-none hover:text-slate-700"
                      : ""
                  }`}
                >
                  {column.header}
                  {sortKey === column.key && (sortDir === "asc" ? " ▲" : " ▼")}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <SkeletonRows columns={columns.length} />
            ) : (
              paginated.map((row) => (
                <tr
                  key={rowKey(row)}
                  onClick={() => onRowClick?.(row)}
                  className={
                    onRowClick ? "cursor-pointer hover:bg-slate-50" : ""
                  }
                >
                  {columns.map((column) => (
                    <td
                      key={column.key}
                      className="whitespace-nowrap px-4 py-3"
                    >
                      {column.render(row)}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {!loading && sorted.length === 0 && (
        <div className="mt-4">
          <EmptyState title={emptyTitle} description={emptyDescription} />
        </div>
      )}

      {!loading && sorted.length > pageSize && (
        <div className="mt-3 flex items-center justify-between text-sm text-slate-500">
          <span>
            Page {currentPage} of {totalPages} — {sorted.length} results
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={currentPage === 1}
              className="rounded-lg border border-slate-300 px-3 py-1.5 disabled:opacity-40"
            >
              Prev
            </button>
            <button
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={currentPage === totalPages}
              className="rounded-lg border border-slate-300 px-3 py-1.5 disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
