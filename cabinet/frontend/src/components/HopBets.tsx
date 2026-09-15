import BetSpot from "./BetSpot";
import { HOP_COMBOS } from "../constants";
import type { BetAreaProps } from "../types";

export default function HopBets({ state, fire, selectedChip }: BetAreaProps) {
  return (
    <div className="hop-grid">
      {HOP_COMBOS.map(([a, b]) => {
        const key = `hop_${a}${b}`;
        const payFor = a === b ? 31 : 16;
        return (
          <BetSpot key={key} spotKey={key} className="hop-spot" state={state} fire={fire} selectedChip={selectedChip}>
            <div className="combo">{a}-{b}</div>
            <div className="pay">{payFor - 1}:1</div>
          </BetSpot>
        );
      })}
    </div>
  );
}
