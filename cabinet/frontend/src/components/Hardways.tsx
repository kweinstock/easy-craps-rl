import DiceIcon from "./DiceIcon";
import BetSpot from "./BetSpot";
import { HARDS } from "../constants";
import type { BetAreaProps } from "../types";

export default function Hardways({ state, fire, selectedChip }: BetAreaProps) {
  return (
    <div className="hardways-grid">
      {HARDS.map((h) => (
        <BetSpot
          key={h.sum}
          spotKey={`hard_${h.sum}`}
          className="hard-spot"
          state={state}
          fire={fire}
          selectedChip={selectedChip}
        >
          <div className="hard-dice">
            <DiceIcon face={h.combo[0]} />
            <DiceIcon face={h.combo[1]} />
          </div>
          <div className="hard-info">
            <div className="since-pill">#{state.hard_since[h.sum]}</div>
            <div className="pay">{h.payFor - 1} TO 1</div>
          </div>
        </BetSpot>
      ))}
    </div>
  );
}
