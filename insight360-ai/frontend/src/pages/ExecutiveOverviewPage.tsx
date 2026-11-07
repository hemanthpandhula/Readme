import { useEffect, useState } from "react";
import { api } from "../api/client";
import { RevenueTrendChart } from "../charts/RevenueTrendChart";

export default function ExecutiveOverviewPage() {
  const [summary, setSummary] = useState<any>();
  const [trends, setTrends] = useState<any[]>([]);
  const [error, setError] = useState<string>();

  useEffect(() => {
    Promise.all([api.get("/dashboard/summary"), api.get("/dashboard/trends")])
      .then(([s, t]) => {
        setSummary(s.data);
        setTrends(t.data);
      })
      .catch((e) => setError(e?.response?.data?.detail ?? "Failed to load dashboard"));
  }, []);

  if (error) return <div className="card">{error}</div>;
  if (!summary) return <div className="card">Loading dashboard...</div>;

  return (
    <div className="space-y-4">
      <div className="grid md:grid-cols-3 gap-4">
        <div className="card">Revenue: {Number(summary.total_revenue).toLocaleString()}</div>
        <div className="card">Profit: {Number(summary.total_profit).toLocaleString()}</div>
        <div className="card">Margin: {Number(summary.profit_margin_pct).toFixed(2)}%</div>
      </div>
      <RevenueTrendChart data={trends} />
    </div>
  );
}
