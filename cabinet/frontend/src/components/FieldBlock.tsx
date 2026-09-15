import BetSpot from "./BetSpot";
import type { BetAreaProps } from "../types";

export default function FieldBlock({ state, fire, selectedChip }: BetAreaProps) {
  return (
    <div className="right-col">
      <div className="field-block">
        <div className="field-title">ONE ROLL BETS</div>
        <div style={{ textAlign: "center", fontWeight: 800, color: "var(--cream)", fontSize: ".8rem", marginBottom: 4 }}>
          FIELD
        </div>
        <BetSpot spotKey="field" className="field-main" state={state} fire={fire} selectedChip={selectedChip}>
          <div className="field-corner"><span>2</span><small>PAYS DOUBLE</small></div>
          <div className="field-nums">
            <span>3</span><span>4</span><span>9</span><span>10</span><span>11</span>
          </div>
          <div className="field-corner"><span>12</span><small>PAYS DOUBLE</small></div>
        </BetSpot>

        <div className="lowhigh-row">
          <BetSpot spotKey="lowfield" className="lh-spot" state={state} fire={fire} selectedChip={selectedChip}>
            <div className="name">LOW FIELD</div>
            <div className="nums">2 &middot; 3 &middot; 4</div>
            <div className="pay">PAYS 4 TO 1</div>
          </BetSpot>
          <BetSpot spotKey="highfield" className="lh-spot" state={state} fire={fire} selectedChip={selectedChip}>
            <div className="name">HIGH FIELD</div>
            <div className="nums">10 &middot; 11 &middot; 12</div>
            <div className="pay">PAYS 4 TO 1</div>
          </BetSpot>
        </div>

        <div className="passline-block">
          <BetSpot spotKey="pass" className="passline-spot" state={state} fire={fire} selectedChip={selectedChip}>
            <div className="passline-title">PASS LINE</div>
            <div className={`odds-hint${state.point !== null ? " show" : ""}`}>tap again to take odds</div>
          </BetSpot>
        </div>
      </div>
    </div>
  );
}
