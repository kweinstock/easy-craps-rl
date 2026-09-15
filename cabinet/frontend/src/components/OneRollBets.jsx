import { useState } from "react";
import DiceIcon from "./DiceIcon.jsx";
import BetSpot from "./BetSpot.jsx";
import Hardways from "./Hardways.jsx";
import HopBets from "./HopBets.jsx";
import { HORN } from "../constants.js";

export default function OneRollBets({ state, fire, selectedChip }) {
  const [tab, setTab] = useState("hardways");
  const hopTotal = Object.entries(state.bets)
    .filter(([k]) => k.startsWith("hop_"))
    .reduce((sum, [, v]) => sum + v, 0);
  const hardTotal = ["hard_4", "hard_6", "hard_8", "hard_10"]
    .reduce((sum, k) => sum + (state.bets[k] || 0), 0);

  return (
    <div className="left-col">
      <div className="tabs">
        <div
          className={`tab ${tab === "hardways" ? "active" : "inactive"}`}
          onClick={() => setTab("hardways")}
        >
          HARDWAYS <span className="amt">${hardTotal.toFixed(2)}</span>
        </div>
        <div
          className={`tab ${tab === "hop" ? "active" : "inactive"}`}
          onClick={() => setTab("hop")}
        >
          HOP BETS <span className="amt">${hopTotal.toFixed(2)}</span>
        </div>
      </div>

      <div className="panel">
        <div className="panel-title">
          {tab === "hardways" ? "HARD WAYS (# of rolls since last)" : "HOP BETS (exact dice combo)"}
        </div>
        {tab === "hardways" ? (
          <Hardways state={state} fire={fire} selectedChip={selectedChip} />
        ) : (
          <HopBets state={state} fire={fire} selectedChip={selectedChip} />
        )}
      </div>

      <div className="panel">
        <div className="panel-title">ONE ROLL BETS</div>
        <BetSpot spotKey="seven" className="seven-row" state={state} fire={fire} selectedChip={selectedChip}>
          <span className="pay"><DiceIcon face={3} small />4 TO 1</span>
          <span className="mid">SEVEN</span>
          <span className="pay">4 TO 1<DiceIcon face={4} small /></span>
        </BetSpot>

        <div className="horn-grid">
          {HORN.map((h) => (
            <BetSpot
              key={h.sum}
              spotKey={`horn_${h.sum}`}
              className="horn-cell"
              state={state}
              fire={fire}
              selectedChip={selectedChip}
            >
              <DiceIcon face={h.combo[0]} />
              <DiceIcon face={h.combo[1]} />
              <span className="pay">{h.payFor - 1} TO 1</span>
            </BetSpot>
          ))}
          <BetSpot spotKey="horn" className="horn-center" state={state} fire={fire} selectedChip={selectedChip}>
            HORN<br />BET
          </BetSpot>
        </div>

        <BetSpot spotKey="anycraps" className="anycraps-row" state={state} fire={fire} selectedChip={selectedChip}>
          <span className="pay"><DiceIcon face={1} small />7 TO 1</span>
          <span className="mid">ANY CRAPS</span>
          <span className="pay">7 TO 1<DiceIcon face={6} small /></span>
        </BetSpot>
      </div>
    </div>
  );
}
