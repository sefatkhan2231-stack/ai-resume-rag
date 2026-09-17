interface SkillListProps {
  skills: Record<string, boolean>;
}

export default function SkillList({ skills }: SkillListProps) {
  const entries = Object.entries(skills);

  return (
    <ul className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-2">
      {entries.map(([skill, matched]) => (
        <li
          key={skill}
          className={`flex items-center gap-2 rounded-lg px-3 py-2 text-sm ${
            matched
              ? "bg-emerald-50 text-emerald-800"
              : "bg-red-50 text-red-800"
          }`}
        >
          <span>{matched ? "✓" : "✗"}</span>
          <span>{skill}</span>
        </li>
      ))}
    </ul>
  );
}
