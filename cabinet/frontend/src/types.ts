// Mirrors the JSON shapes from cabinet/backend/app/api/main.py and
// easycraps/src/easycraps/engine/state.py (GameState.to_dict / RollResult).
// Keep this in sync with the backend — it's the one contract the whole
// frontend is typed against.

export interface RollResult {
  dice: [number, number];
  total: number;
  winnings: number;
  resolved: Record<string, number>;
  lost_keys: string[];
  point_before: number | null;
  point_after: number | null;
}

export interface LuckyHits {
  lowrolls: number[];
  rollemall: number[];
  highrolls: number[];
}

export interface GameState {
  credit: number;
  bets: Record<string, number>;
  total_bets: number;
  point: number | null;
  min_bet: number;
  set_bets_on: boolean;
  puck_manual_off: boolean;
  hard_since: Record<string, number>;
  lucky_hits: LuckyHits;
  history: [number, number][];
  bet_log_count: number;
  message: string;
  last_roll: RollResult | null;
}

export interface TriggerResponse {
  ok: boolean;
  message: string;
  state: GameState;
}

export interface NewSessionResponse {
  session_id: string;
  state: GameState;
}

/** Payload shape accepted by every trigger — see backend/README.md. */
export type TriggerPayload = Record<string, string | number | boolean | undefined>;

export type FireTrigger = (trigger: string, payload?: TriggerPayload) => void;

/** Shared props every bet-area component takes from GamePage. */
export interface BetAreaProps {
  state: GameState;
  fire: FireTrigger;
  selectedChip: number;
}
