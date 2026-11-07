import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

export function RevenueTrendChart({ data }: { data: any[] }) {
  return (
    <div className="card h-80">
      <h2 className="font-semibold mb-2">Monthly Revenue Trend</h2>
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={data}>
          <XAxis dataKey="period_start" />
          <YAxis />
          <Tooltip />
          <Line dataKey="revenue" stroke="#22d3ee" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
