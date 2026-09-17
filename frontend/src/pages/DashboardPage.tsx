import { useEffect, useState } from "react";
import { getDashboardActivity, getDashboardStats } from "../api/dashboardApi";
import ActivityChart from "../components/ActivityChart";
import ErrorState from "../components/ErrorState";
import StatCard from "../components/StatCard";
import type { ActivityPoint, DashboardStats } from "../types";

const TECH_STACK = [
  {
    category: "NLP / Embeddings",
    items: ["Sentence Transformers", "all-MiniLM-L6-v2"],
    description:
      "Converts resume text into numerical vector representations so semantically similar content can be compared.",
  },
  {
    category: "Vector Database",
    items: ["ChromaDB"],
    description:
      "Stores resume embeddings and enables semantic retrieval of relevant resume information.",
  },
  {
    category: "Reranking",
    items: ["Cross-Encoder (ms-marco-MiniLM-L-6-v2)"],
    description:
      "Re-ranks retrieved resume chunks based on their relevance to the query.",
  },
  {
    category: "LLM",
    items: ["Ollama", "Llama 3.2 (configurable via OLLAMA_MODEL)"],
    description:
      "Generates evidence-based responses from the retrieved resume information.",
  },
  {
    category: "Backend",
    items: ["FastAPI", "Python", "SQLAlchemy / SQLite"],
    description:
      "Serves the API and persists candidates and screening history.",
  },
  {
    category: "Frontend",
    items: ["React", "TypeScript", "Tailwind CSS"],
    description: "The interface you're using right now.",
  },
];

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [activity, setActivity] = useState<ActivityPoint[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      setLoading(true);
      setError(null);
      try {
        const [statsData, activityData] = await Promise.all([
          getDashboardStats(),
          getDashboardActivity(30),
        ]);
        if (!cancelled) {
          setStats(statsData);
          setActivity(activityData);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : "Failed to load dashboard data.",
          );
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
      <p className="mt-1 text-sm text-slate-500">
        Overview of the AI resume screening system.
      </p>

      {error && (
        <div className="mt-6">
          <ErrorState message={error} />
        </div>
      )}

      {!error && (
        <>
          <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
            {loading || !stats ? (
              Array.from({ length: 7 }).map((_, i) => (
                <div
                  key={i}
                  className="h-24 animate-pulse rounded-xl bg-slate-200"
                />
              ))
            ) : (
              <>
                <StatCard label="Total Resumes" value={stats.total_resumes} />
                <StatCard label="Today" value={stats.resumes_today} />
                <StatCard label="This Week" value={stats.resumes_this_week} />
                <StatCard label="This Month" value={stats.resumes_this_month} />
                <StatCard label="This Year" value={stats.resumes_this_year} />
                <StatCard
                  label="Total Screenings"
                  value={stats.total_screenings}
                />
                <StatCard
                  label="Avg Match Score"
                  value={`${stats.average_match_score}%`}
                />
              </>
            )}
          </div>

          <div className="mt-8 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-sm font-semibold text-slate-800">
              Screening Activity (last 30 days)
            </h2>
            <div className="mt-4">
              {loading ? (
                <div className="h-64 animate-pulse rounded-lg bg-slate-100" />
              ) : (
                <ActivityChart data={activity} />
              )}
            </div>
          </div>
        </>
      )}

      <div className="mt-8">
        <h2 className="text-sm font-semibold text-slate-800">
          AI Technology Stack
        </h2>
        <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {TECH_STACK.map((tech) => (
            <div
              key={tech.category}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                {tech.category}
              </p>
              <div className="mt-2 flex flex-wrap gap-1.5">
                {tech.items.map((item) => (
                  <span
                    key={item}
                    className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-700"
                  >
                    {item}
                  </span>
                ))}
              </div>
              <p className="mt-3 text-sm text-slate-500">{tech.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
