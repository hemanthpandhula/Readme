import { useEffect, useState } from "react";
import { api } from "../api/client";
import { TablePage } from "./TablePage";

export function DataPageFactory({ title, endpoint }: { title: string; endpoint: string }) {
  const [rows, setRows] = useState<any[]>([]);
  const [error, setError] = useState<string>();

  useEffect(() => {
    api.get(endpoint)
      .then((r) => setRows(r.data))
      .catch((e) => setError(e?.response?.data?.detail ?? `Failed to load ${title}`));
  }, [endpoint, title]);

  if (error) return <div className="card">{error}</div>;
  if (!rows.length) return <div className="card">Loading {title}...</div>;
  return <TablePage title={title} rows={rows} />;
}
