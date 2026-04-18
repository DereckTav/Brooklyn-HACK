import { useState } from "react";
import { useGameStore } from "../store/gameStore";

export default function APDiceRoll() {
  const open = useGameStore((s) => s.diceModalOpen);
  const turn = useGameStore((s) => s.turn);
  const rollAP = useGameStore((s) => s.rollAP);

  const [rolling, setRolling] = useState(false);
  const [result, setResult] = useState<number | null>(null);

  if (!open) return null;

  const roll = async () => {
    setRolling(true);
    setResult(null);

    // Visual spin for 1.4s, then fetch the real AP from the backend
    window.setTimeout(async () => {
      await rollAP(); // This calls the backend and sets AP in the store
      // Read the AP that was just set in the store
      const ap = useGameStore.getState().ap;
      setRolling(false);
      setResult(ap);
    }, 1400);
  };

  const proceed = () => {
    if (result == null) return;
    setResult(null);
    // AP is already set from rollAP — just close the modal
    useGameStore.setState({ diceModalOpen: false });
  };

  return (
    <div className="dice-overlay">
      <div className="dice-modal">
        <h2 className="dice-modal__title">TURN {turn}</h2>
        <p className="dice-modal__sub">Roll for Action Points</p>
        <div className={`dice ${rolling ? "dice--spinning" : ""}`}>
          <span className="dice__face">{rolling ? "?" : (result ?? "?")}</span>
        </div>
        {result == null ? (
          <button
            className="btn btn--primary"
            onClick={roll}
            disabled={rolling}
          >
            {rolling ? "ROLLING..." : "ROLL"}
          </button>
        ) : (
          <>
            <div className="dice-modal__result">+{result} ACTION POINTS</div>
            <button className="btn btn--primary" onClick={proceed}>
              PROCEED
            </button>
          </>
        )}
      </div>
    </div>
  );
}
