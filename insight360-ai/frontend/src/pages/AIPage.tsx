import { useState } from "react";
import { api } from "../api/client";

export default function AIPage() {
  const [question, setQuestion] = useState("Why did profit decrease?");
  const [messages, setMessages] = useState<any[]>([]);

  const ask = async () => {
    const userMsg = { role: "user", text: question };
    setMessages((m) => [...m, userMsg]);
    try {
      const res = await api.post("/ai/chat", { question });
      setMessages((m) => [...m, { role: "assistant", text: res.data.answer, evidence: res.data.evidence }]);
    } catch (e: any) {
      setMessages((m) => [...m, { role: "assistant", text: e?.response?.data?.detail ?? "Request failed" }]);
    }
  };

  return (
    <div className="space-y-4">
      <div className="card space-y-2">
        <input className="w-full bg-slate-800 rounded p-2" value={question} onChange={(e) => setQuestion(e.target.value)} />
        <button className="bg-cyan-600 px-4 py-2 rounded" onClick={ask}>Ask</button>
      </div>
      <div className="card space-y-3">
        {messages.map((m, i) => (
          <div key={i}>
            <p className="font-semibold">{m.role}</p>
            <p>{m.text}</p>
            {m.evidence ? <pre className="text-xs overflow-auto">{JSON.stringify(m.evidence, null, 2)}</pre> : null}
          </div>
        ))}
        {!messages.length && <p>No messages yet.</p>}
      </div>
    </div>
  );
}
