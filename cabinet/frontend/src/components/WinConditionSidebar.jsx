import { winningNumbersForSpot } from "../constants.js";

const NUMS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

export default function WinConditionSidebar({ state }) {
  const winningNumbers = new Set();
  Object.keys(state.bets).forEach((spotKey) => {
    winningNumbersForSpot(spotKey, state.point).forEach((n) => winningNumbers.add(n));
  });

  return (
    <div className="wincond-sidebar">
      <div className="wincond-title">WIN<br />CONDITION</div>
      <div className="wincond-list">
        {NUMS.map((n) => (
          <div key={n} className={`wincond-item${winningNumbers.has(n) ? " hit" : ""}`}>
            <div className="wincond-num">{n}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
