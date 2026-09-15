import DiceIcon from "./DiceIcon";
import type { GameState } from "../types";

interface HistoryBarProps {
  state: GameState;
}

export default function HistoryBar({ state }: HistoryBarProps) {
  const items = [...state.history].reverse().slice(0, 14);
  return (
    <div className="historybar">
      {items.map(([d1, d2], i) => (
        <div className="hist-item" key={i}>
          <div className="hist-dice">
            <DiceIcon face={d1} small />
            <DiceIcon face={d2} small />
          </div>
          <div className="hist-sum">{d1 + d2}</div>
        </div>
      ))}
      <div className="hist-arrow">&#9656;</div>
    </div>
  );
}
