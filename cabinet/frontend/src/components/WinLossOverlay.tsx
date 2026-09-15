import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import type { RollResult } from "../types";

const WIN_COUNT_MS = 900;
const WIN_HOLD_MS = 1200;
const LOSE_HOLD_MS = 1200;
const TICK_MS = 16;

interface WinLossOverlayProps {
  lastRoll: RollResult | null;
  rollSeq: number;
}

type Display = { type: "win"; amount: number } | { type: "lose" } | null;

// Flashes a big overlay after each resolved roll: gold text counting up to
// the amount won, or a plain "YOU LOST" when nothing was won but something
// on the table lost. `rollSeq` (state.history.length) tells us a new roll
// happened even if the winnings/lost_keys look the same as last time.
//
// Uses setInterval rather than requestAnimationFrame for the count-up:
// rAF is paused entirely while the tab/pane isn't visible, which would
// silently swallow the very first frame (and the whole animation) whenever
// the cabinet isn't the focused tab.
export default function WinLossOverlay({ lastRoll, rollSeq }: WinLossOverlayProps) {
  const [display, setDisplay] = useState<Display>(null);
  const seenSeq = useRef<number | null>(null);

  useEffect(() => {
    if (rollSeq == null || rollSeq === seenSeq.current) return;
    seenSeq.current = rollSeq;
    if (!lastRoll) return;

    const won = lastRoll.winnings > 0;
    const lost = !won && (lastRoll.lost_keys || []).length > 0;
    if (!won && !lost) return;

    if (!won) {
      setDisplay({ type: "lose" });
      const hideTimer = setTimeout(() => setDisplay(null), LOSE_HOLD_MS);
      return () => clearTimeout(hideTimer);
    }

    const target = lastRoll.winnings;
    const start = performance.now();
    setDisplay({ type: "win", amount: 0 });
    const interval = setInterval(() => {
      const t = Math.min(1, (performance.now() - start) / WIN_COUNT_MS);
      const eased = 1 - Math.pow(1 - t, 3);
      setDisplay({ type: "win", amount: eased * target });
      if (t >= 1) clearInterval(interval);
    }, TICK_MS);
    const hideTimer = setTimeout(() => setDisplay(null), WIN_COUNT_MS + WIN_HOLD_MS);
    return () => {
      clearInterval(interval);
      clearTimeout(hideTimer);
    };
  }, [rollSeq, lastRoll]);

  if (!display) return null;

  return createPortal(
    <div className="winloss-overlay">
      {display.type === "win" ? (
        <div className="winloss-text win">YOU WON<br />${display.amount.toFixed(2)}</div>
      ) : (
        <div className="winloss-text lose">YOU LOST</div>
      )}
    </div>,
    document.body
  );
}
