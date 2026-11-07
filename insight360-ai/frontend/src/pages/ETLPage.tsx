import { useState } from "react";
import { api } from "../api/client";

export default function ETLPage() {
  const [status, setStatus] = useState<string>("");

  const run = async () => {
    setStatus("Running ETL...");
    try {
      const res = await api.post("/etl/run?mode=full");
      setStatus(res.data.detail);
    } catch (e: any) {
      setStatus(e?.response?.data?.detail ?? "ETL failed");
    }
  };

  return (
    <div className="space-y-4">
      <div className="card">
        <button className="bg-cyan-600 px-4 py-2 rounded" onClick={run}>Run Full ETL</button>
      </div>
      <div className="card">{status || "No run started"}</div>
    </div>
  );
}
