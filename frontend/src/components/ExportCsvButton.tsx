import { getExportUrl } from "../api/resultsApi";

interface ExportCsvButtonProps {
  screeningId: number | null;
}

export default function ExportCsvButton({ screeningId }: ExportCsvButtonProps) {
  if (screeningId === null) return null;

  return (
    <a
      href={getExportUrl(screeningId)}
      download
      className="inline-flex items-center gap-2 rounded-lg border border-slate-300 bg-white px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
    >
      Export CSV
    </a>
  );
}
