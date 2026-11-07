import { Link, Outlet } from "react-router-dom";

const items = [
  ["/login", "Login / Demo Access"],
  ["/", "Executive Overview"],
  ["/sales", "Sales Analytics"],
  ["/customers", "Customer Intelligence"],
  ["/products", "Product Performance"],
  ["/regions", "Regional Analytics"],
  ["/finance", "Financial Analytics"],
  ["/etl", "ETL Monitor"],
  ["/quality", "Data Quality"],
  ["/anomalies", "Anomaly Detection"],
  ["/forecast", "Revenue Forecasting"],
  ["/ai", "AI Assistant"],
  ["/settings", "Settings"],
];

export function Layout() {
  return (
    <div className="min-h-screen md:grid md:grid-cols-[260px_1fr]">
      <aside className="p-4 border-r border-slate-800">
        <h1 className="text-xl font-bold mb-4">Insight360 AI</h1>
        <nav className="flex flex-col gap-2">
          {items.map(([to, label]) => (
            <Link key={to} to={to} className="rounded px-3 py-2 hover:bg-slate-800">
              {label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="p-4 md:p-6">
        <Outlet />
      </main>
    </div>
  );
}
