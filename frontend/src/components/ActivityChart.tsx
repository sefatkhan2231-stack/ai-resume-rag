import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { ActivityPoint } from "../types";

interface ActivityChartProps {
  data: ActivityPoint[];
}

export default function ActivityChart({ data }: ActivityChartProps) {
  if (!data.length) {
    return (
      <div className="flex h-64 items-center justify-center text-sm text-slate-400">
        No screening activity yet.
      </div>
    );
  }

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="#e2e8f0"
            vertical={false}
          />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} stroke="#94a3b8" />
          <YAxis
            allowDecimals={false}
            tick={{ fontSize: 12 }}
            stroke="#94a3b8"
          />
          <Tooltip
            contentStyle={{
              borderRadius: 8,
              borderColor: "#e2e8f0",
              fontSize: 13,
            }}
            labelStyle={{ fontWeight: 600 }}
          />
          <Bar
            dataKey="count"
            name="Screenings"
            fill="#0f172a"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
