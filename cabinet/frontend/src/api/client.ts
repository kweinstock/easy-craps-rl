// Thin client over the Easy Craps backend. Every UI action calls fireTrigger()
// with the same trigger names an RL agent would use — see backend/README.md.
import type { GameState, NewSessionResponse, TriggerPayload, TriggerResponse } from "../types";

const API_BASE: string = import.meta.env.VITE_API_BASE || "/api";

export async function createSession(): Promise<NewSessionResponse> {
  const res = await fetch(`${API_BASE}/sessions`, { method: "POST" });
  if (!res.ok) throw new Error(`createSession failed: ${res.status}`);
  return res.json();
}

export async function getState(sessionId: string): Promise<GameState> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/state`);
  if (!res.ok) throw new Error(`getState failed: ${res.status}`);
  return res.json();
}

export async function fireTrigger(
  sessionId: string,
  trigger: string,
  payload: TriggerPayload = {}
): Promise<TriggerResponse> {
  const res = await fetch(`${API_BASE}/sessions/${sessionId}/trigger`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ trigger, payload }),
  });
  const body = await res.json().catch(() => null);
  if (!res.ok) {
    const detail = body && body.detail ? body.detail : `trigger ${trigger} failed`;
    throw new Error(detail);
  }
  return body;
}

export function wsUrl(sessionId: string): string {
  const httpBase = API_BASE.startsWith("http")
    ? API_BASE
    : `${window.location.origin}${API_BASE}`;
  const url = new URL(`${httpBase}/sessions/${sessionId}/ws`);
  url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
  return url.toString();
}
