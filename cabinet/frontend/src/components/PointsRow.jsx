import BetSpot from "./BetSpot.jsx";
import { POINT_NUMBERS, POINT_LABEL, PLACE_PAY } from "../constants.js";

export default function PointsRow({ state, fire, selectedChip }) {
  return (
    <>
      <div className="plp-label">PASS LINE POINT</div>
      <div className="points-row">
        {POINT_NUMBERS.map((n) => {
          const [a, b] = PLACE_PAY[n];
          const label = POINT_LABEL[n];
          const isPoint = state.point === n;
          return (
            <BetSpot
              key={n}
              spotKey={`place_${n}`}
              className={`point-box${isPoint ? " is-point" : ""}`}
              state={state}
              fire={fire}
              selectedChip={selectedChip}
            >
              <div className="puck">ON</div>
              <div className={`num${label.length > 2 ? " word" : ""}`}>{label}</div>
              <div className="pays">PAYS<b>{a - b} TO {b}</b></div>
            </BetSpot>
          );
        })}
      </div>
      <div className="place-label">PLACE BETS</div>
    </>
  );
}
