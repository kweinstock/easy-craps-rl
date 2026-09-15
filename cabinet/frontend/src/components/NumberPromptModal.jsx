import { useState } from "react";
import { createPortal } from "react-dom";

// A touchscreen-friendly stand-in for window.prompt() — native browser
// dialogs don't render well (or at all) in kiosk/embedded webviews.
//
// Rendered via a portal straight to document.body: the cabinet's own
// stacking contexts (.ctrl-bar and .felt-body both sit at z-index:1, and
// .felt-body comes later in the DOM, so it always painted on top of any
// overlay nested inside .ctrl-bar no matter what z-index the overlay used
// locally). A portal escapes that entirely instead of trying to out-stack
// the rest of the cabinet.
export default function NumberPromptModal({ title, defaultValue, onSubmit, onCancel }) {
  const [value, setValue] = useState(String(defaultValue ?? ""));

  function submit() {
    const num = parseFloat(value);
    if (!num || num <= 0) return;
    onSubmit(num);
  }

  return createPortal(
    <div
      style={{
        position: "fixed", inset: 0, background: "rgba(0,0,0,.6)",
        display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000,
      }}
      onClick={onCancel}
    >
      <div
        style={{
          background: "#13210f", border: "1px solid var(--border)", borderRadius: 10,
          padding: 20, minWidth: 240, color: "var(--cream)",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ fontWeight: 800, marginBottom: 10 }}>{title}</div>
        <input
          type="number"
          autoFocus
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && submit()}
          style={{ width: "100%", padding: 8, borderRadius: 6, border: "1px solid #999", marginBottom: 12, fontSize: "1rem" }}
        />
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <div className="tray-btn" onClick={onCancel}>CANCEL</div>
          <div className="tray-btn" onClick={submit}>OK</div>
        </div>
      </div>
    </div>,
    document.body
  );
}
