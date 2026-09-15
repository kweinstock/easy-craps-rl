import { useGame } from "../hooks/useGame";
import ControlBar from "../components/ControlBar";
import SubMeters from "../components/SubMeters";
import LuckyRoller from "../components/LuckyRoller";
import WinConditionSidebar from "../components/WinConditionSidebar";
import PointsRow from "../components/PointsRow";
import OneRollBets from "../components/OneRollBets";
import MidCol from "../components/MidCol";
import FieldBlock from "../components/FieldBlock";
import HistoryBar from "../components/HistoryBar";
import MessageToast from "../components/MessageToast";
import ChipTray from "../components/ChipTray";
import WinLossOverlay from "../components/WinLossOverlay";

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
