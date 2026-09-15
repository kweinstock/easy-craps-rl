import { CHIP_VALUES } from "../constants.js";

export default function ChipTray({ state, fire, selectedChip, setSelectedChip }) {
  const clearLabel = state.bet_log_count === 0 ? "CLEAR\nALL BETS" : "CLEAR\nLAST BET";
  const canRoll = state.total_bets >= state.min_bet;

  function onClear() {
    fire(state.bet_log_count === 0 ? "clear_all_bets" : "clear_last_bet");
  }

  return (
    <div className="traybar">
      <div className="tray-btn" onClick={onClear}>
        <span className="ic">&#10060;</span>
        <span>
          {clearLabel.split("\n").map((line, i) => (
            <span key={i}>{line}<br /></span>
          ))}
        </span>
      </div>
      <div className="chip-rack">
        {CHIP_VALUES.map((v) => (
          <div
            key={v}
            className={`chip c${v}${selectedChip === v ? " selected" : ""}`}
            onClick={() => setSelectedChip(v)}
          >
            ${v}
          </div>
        ))}
      </div>
      <div className="tray-btn" onClick={() => fire("double_bet")}>
        <span className="ic">&#10006;2</span>DOUBLE<br />BET
      </div>
      <div className="tray-btn" onClick={() => fire("repeat_last_bet")}>
        <span className="ic">&#8635;</span>REPEAT<br />LAST BET
      </div>
      <div className={`roll-btn${canRoll ? "" : " disabled"}`} onClick={() => canRoll && fire("roll")}>
        ROLL
      </div>
    </div>
  );
}
