export default function SubMeters({ state }) {
  return (
    <div className="sub-meters">
      <div className="meter-big">
        <div className="lbl">PLAYABLE:</div>
        <div className="val">${state.credit.toFixed(2)}</div>
      </div>
      <div className="meter-big">
        <div className="lbl">BET:</div>
        <div className="val">${state.total_bets.toFixed(2)}</div>
      </div>
    </div>
  );
}
