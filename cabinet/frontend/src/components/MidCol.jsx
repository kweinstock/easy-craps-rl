import BetSpot from "./BetSpot.jsx";

export default function MidCol({ state, fire, selectedChip }) {
  return (
    <div className="mid-col">
      <div className="ce-stack">
        <BetSpot spotKey="c" className="ce-circle" state={state} fire={fire} selectedChip={selectedChip}>C</BetSpot>
        <BetSpot spotKey="ce" className="ce-circle big" state={state} fire={fire} selectedChip={selectedChip}>C&amp;E</BetSpot>
        <BetSpot spotKey="e" className="ce-circle" state={state} fire={fire} selectedChip={selectedChip}>E</BetSpot>
      </div>
      <div className="btn-stack">
        <div
          className={`special-btn setbets${!state.set_bets_on ? " active" : ""}`}
          onClick={() => fire("toggle_set_bets")}
        >
          {state.set_bets_on ? "SET BETS ON" : "SET BETS OFF"}
        </div>
        <div className="special-btn pa" onClick={() => fire("press")}>PRESS</div>
        <div className="special-btn pa" onClick={() => fire("across", { amount: selectedChip })}>ACROSS</div>
      </div>
    </div>
  );
}
