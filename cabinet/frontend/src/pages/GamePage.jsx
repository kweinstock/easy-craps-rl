import { useGame } from "../hooks/useGame.js";
import ControlBar from "../components/ControlBar.jsx";
import SubMeters from "../components/SubMeters.jsx";
import LuckyRoller from "../components/LuckyRoller.jsx";
import WinConditionSidebar from "../components/WinConditionSidebar.jsx";
import PointsRow from "../components/PointsRow.jsx";
import OneRollBets from "../components/OneRollBets.jsx";
import MidCol from "../components/MidCol.jsx";
import FieldBlock from "../components/FieldBlock.jsx";
import HistoryBar from "../components/HistoryBar.jsx";
import MessageToast from "../components/MessageToast.jsx";
import ChipTray from "../components/ChipTray.jsx";
import WinLossOverlay from "../components/WinLossOverlay.jsx";

export default function GamePage() {
  const { state, connected, fire, selectedChip, setSelectedChip } = useGame();

  if (!state) {
    return <div className="cabinet"><div className="screen"><p style={{ color: "#fff", padding: 20 }}>Connecting to table…</p></div></div>;
  }

  return (
    <div className="cabinet">
      <WinLossOverlay lastRoll={state.last_roll} rollSeq={state.history.length} />
      <div className="screen">
        {!connected && <div className="conn-banner">Reconnecting to table…</div>}
        <ControlBar state={state} fire={fire} />
        <SubMeters state={state} />
        <div className="felt-body">
          <LuckyRoller state={state} fire={fire} selectedChip={selectedChip} />

          <div className="middle-grid">
            <div className="middle-left">
              <div className="gamearea-grid">
                <OneRollBets state={state} fire={fire} selectedChip={selectedChip} />
                <div className="right-stack">
                  <PointsRow state={state} fire={fire} selectedChip={selectedChip} />
                  <div className="game-cols">
                    <MidCol state={state} fire={fire} selectedChip={selectedChip} />
                    <FieldBlock state={state} fire={fire} selectedChip={selectedChip} />
                  </div>
                </div>
              </div>
            </div>
            <WinConditionSidebar state={state} />
          </div>

          <HistoryBar state={state} />
          <MessageToast message={state.message} />

          <ChipTray
            state={state}
            fire={fire}
            selectedChip={selectedChip}
            setSelectedChip={setSelectedChip}
          />
        </div>
      </div>
    </div>
  );
}
