import { useCallback, useEffect, useRef, useState } from "react";
import { createSession, wsUrl } from "../api/client";
import type { FireTrigger, GameState, TriggerPayload, TriggerResponse } from "../types";

export interface UseGameResult {
  sessionId: string | null;
  state: GameState | null;
  connected: boolean;
  fire: FireTrigger;
  selectedChip: number;
  setSelectedChip: (chip: number) => void;
}

// Drives one Easy Craps session: opens the session, keeps a live WebSocket
// connection to it, and exposes fire(trigger, payload) for every button —
// the same trigger names an RL agent would call over the REST API.
export function useGame(): UseGameResult {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [state, setState] = useState<GameState | null>(null);
  const [connected, setConnected] = useState(false);
  const [selectedChip, setSelectedChip] = useState(1);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    let cancelled = false;
    createSession().then(({ session_id, state }) => {
      if (cancelled) return;
      setSessionId(session_id);
      setState(state);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!sessionId) return undefined;
    const ws = new WebSocket(wsUrl(sessionId));
    wsRef.current = ws;
    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);
    ws.onerror = () => setConnected(false);
    ws.onmessage = (evt) => {
      const body: TriggerResponse = JSON.parse(evt.data);
      setState(body.state);
    };
    return () => ws.close();
  }, [sessionId]);

  const fire = useCallback<FireTrigger>((trigger, payload: TriggerPayload = {}) => {
    const ws = wsRef.current;
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ trigger, payload }));
    }
  }, []);

  return { sessionId, state, connected, fire, selectedChip, setSelectedChip };
}
