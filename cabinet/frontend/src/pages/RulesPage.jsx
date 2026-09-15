import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { marked } from "marked";

const API_BASE = import.meta.env.VITE_API_BASE || "/api";

export default function RulesPage() {
  const [html, setHtml] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/rules`)
      .then((res) => {
        if (!res.ok) throw new Error(`Failed to load rulebook (${res.status})`);
        return res.text();
      })
      .then((md) => setHtml(marked.parse(md)))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="rules-page">
      <Link className="rules-back" to="/">&larr; Back to the table</Link>
      {error && <p>Could not load the rulebook: {error}</p>}
      {!error && !html && <p>Loading rulebook…</p>}
      {html && <div dangerouslySetInnerHTML={{ __html: html }} />}
    </div>
  );
}
