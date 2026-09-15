import { useState } from "react";
import NumberPromptModal from "./NumberPromptModal";
import type { FireTrigger, GameState } from "../types";

interface ControlBarProps {
  state: GameState;
  fire: FireTrigger;
}

type ModalKind = "addFunds" | "minBet" | null;

export default function ControlBar({ state, fire }: ControlBarProps) {
  const [modal, setModal] = useState<ModalKind>(null);

  function onHelp() {
    // Help always opens the rulebook — a real route, not just a toast.
    window.open("/rules", "_blank", "noopener");
  }

  return (
    <div className="ctrl-bar">
      <div className="cashout-block">
        <div className="cashout-btn" onClick={() => fire("cashout")}>CASHOUT</div>
        <div className="credit-stack" onClick={() => setModal("addFunds")}>
          CREDIT<b>${state.credit.toFixed(2)}</b>
        </div>
        <div className="player-badge">
          <span className="av">&#128100;</span><span><b>Player</b></span>
        </div>
      </div>
      <div className="ib-center">Max total bet: ${state.min_bet}</div>
      <div className="top-right-btns">
        <div className="tbtn addfunds" onClick={() => setModal("addFunds")}>+ Add<br />Funds</div>
        <div className="tbtn" onClick={() => setModal("minBet")}>&#9881;</div>
        <div className="tbtn help" onClick={onHelp}>HELP</div>
      </div>

      {modal === "addFunds" && (
        <NumberPromptModal
          title="Add funds ($)"
          defaultValue={20}
          onCancel={() => setModal(null)}
          onSubmit={(num) => {
            fire("add_funds", { amount: num });
            setModal(null);
          }}
        />
      )}
      {modal === "minBet" && (
        <NumberPromptModal
          title="Minimum total bet ($)"
          defaultValue={state.min_bet}
          onCancel={() => setModal(null)}
          onSubmit={(num) => {
            fire("set_min_bet", { amount: num });
            setModal(null);
          }}
        />
      )}
    </div>
  );
}
