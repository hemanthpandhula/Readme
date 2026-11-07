export function TablePage({ title, rows }: { title: string; rows: any[] }) {
  return (
    <div className="card overflow-auto">
      <h2 className="font-semibold mb-3">{title}</h2>
      <table className="w-full text-sm">
        <thead>
          <tr>
            {rows[0] ? Object.keys(rows[0]).map((k) => <th key={k} className="text-left p-2">{k}</th>) : null}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, i) => (
            <tr key={i} className="border-t border-slate-800">
              {Object.values(r).map((v: any, j) => <td key={j} className="p-2">{String(v)}</td>)}
            </tr>
          ))}
        </tbody>
      </table>
      {!rows.length && <p className="text-slate-400">No data available.</p>}
    </div>
  );
}
