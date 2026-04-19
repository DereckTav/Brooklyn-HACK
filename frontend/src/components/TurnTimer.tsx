import { useEffect, useState } from "react";
import { useGameStore } from "../store/gameStore";

export default function TurnTimer() {
  const turnExpiresAt = useGameStore((s) => s.turnExpiresAt);
  const endTurn = useGameStore((s) => s.endTurn);
  const [timeLeft, setTimeLeft] = useState<number | null>(null);

  useEffect(() => {
    if (!turnExpiresAt) {
      setTimeLeft(null);
      return;
    }

    const updateTimer = () => {
      const now = Date.now() / 1000;
      const remaining = Math.max(0, turnExpiresAt - now);
      setTimeLeft(remaining);

      if (remaining <= 0) {
        endTurn();
      }
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);
    return () => clearInterval(interval);
  }, [turnExpiresAt, endTurn]);

  if (timeLeft === null) return null;

  const isDanger = timeLeft < 10;
  const progress = (timeLeft / 40) * 100; // Fixed 40s limit from BALANCE

  return (
    <div className={`turn-timer ${isDanger ? "turn-timer--danger" : ""}`}>
      <div className="turn-timer__label">SESSION TIME</div>
      <div className="turn-timer__clock">
        [ 00:{Math.ceil(timeLeft).toString().padStart(2, "0")} ]
      </div>
      <div className="turn-timer__bar-track">
        <div 
          className="turn-timer__bar-fill" 
          style={{ width: `${progress}%` }} 
        />
      </div>
    </div>
  );
}
