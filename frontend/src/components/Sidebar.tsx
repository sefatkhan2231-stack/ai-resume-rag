import { NavLink } from "react-router-dom";

const LINKS = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/resume-screening", label: "Resume Screening" },
  { to: "/job-matching", label: "Job Matching" },
  { to: "/screening-history", label: "Screening History" },
];

export default function Sidebar() {
  return (
    <aside className="hidden w-60 shrink-0 border-r border-slate-200 bg-white sm:block">
      <div className="px-6 py-5">
        <h1 className="text-base font-bold text-slate-900">
          AI Resume Screening
        </h1>
        <p className="mt-0.5 text-xs text-slate-500">
          RAG-powered candidate evaluation
        </p>
      </div>
      <nav className="flex flex-col gap-1 px-3">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.end}
            className={({ isActive }) =>
              `rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? "bg-slate-900 text-white"
                  : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
              }`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
}
