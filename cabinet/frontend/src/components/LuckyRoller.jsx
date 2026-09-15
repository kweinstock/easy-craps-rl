import BetSpot from "./BetSpot.jsx";

const LOW_NUMS = [2, 3, 4, 5, 6];
const HIGH_NUMS = [8, 9, 10, 11, 12];

function Pips({ nums, hits }) {
  return (
    <div className="lr-pips">
      {nums.map((n) => (
        <div key={n} className={`pip-num${hits.has(n) ? " lit" : ""}`}>{n}</div>
      ))}
    </div>
  );
}

export default function LuckyRoller({ state, fire, selectedChip }) {
  const lastRoll = state.last_roll;
  const lowHits = new Set([...(state.lucky_hits.lowrolls || []), ...(state.lucky_hits.rollemall || [])]);
  const highHits = new Set([...(state.lucky_hits.highrolls || []), ...(state.lucky_hits.rollemall || [])]);

  return (
    <div className="luckyroller">
      <div className="lr-meters">
        <span>LAST BET: <b>${state.total_bets.toFixed(2)}</b></span><br />
        <span>LAST WIN: <b>${(lastRoll?.winnings || 0).toFixed(2)}</b></span>
      </div>
      <div className="lr-body">
        <div className="lr-cols">
          <div className="lr-col">
            <div className="script left">Lucky</div>
            <Pips nums={LOW_NUMS} hits={lowHits} />
            <BetSpot spotKey="lowrolls" className="lr-panel" state={state} fire={fire} selectedChip={selectedChip}>
              <div className="lr-title">LOW ROLLS</div>
              <div className="lr-sub">BET HERE</div>
              <div className="lr-pay">30 <small>TO 1</small></div>
            </BetSpot>
          </div>
          <div className="lr-col">
            <div className="lr-dicegraphic">&#127922;&#127922;</div>
            <div style={{ height: 20 }} />
            <BetSpot spotKey="rollemall" className="lr-panel" state={state} fire={fire} selectedChip={selectedChip}>
              <div className="lr-title">ROLL'EM ALL</div>
              <div className="lr-sub">BET HERE</div>
              <div className="lr-pay">155 <small>TO 1</small></div>
            </BetSpot>
          </div>
          <div className="lr-col">
            <div className="script right">Roller</div>
            <Pips nums={HIGH_NUMS} hits={highHits} />
            <BetSpot spotKey="highrolls" className="lr-panel" state={state} fire={fire} selectedChip={selectedChip}>
              <div className="lr-title">HIGH ROLLS</div>
              <div className="lr-sub">BET HERE</div>
              <div className="lr-pay">30 <small>TO 1</small></div>
            </BetSpot>
          </div>
        </div>
        {state.point === null && (
          <div
            className={`puck-off${state.puck_manual_off ? " on" : ""}`}
            onClick={() => fire("toggle_puck")}
          >
            OFF
          </div>
        )}
      </div>
    </div>
  );
}
