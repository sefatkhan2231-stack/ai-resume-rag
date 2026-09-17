const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api";

export function getExportUrl(screeningId: number): string {
  return `${API_URL}/results/export/${screeningId}`;
}
