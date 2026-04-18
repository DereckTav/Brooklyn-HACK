import { useNavigate } from "react-router-dom";

export default function LaunchPage() {
  const navigate = useNavigate();
  const hasSave = Boolean(localStorage.getItem("mogul_blocks_save"));

  return (
    <main className="launch">
      <h1 className="launch__title">MOGUL BLOCKS</h1>
      <p className="launch__sub">Pop culture is the alpha.</p>

      <div className="launch__buttons">
        <button className="btn btn--primary" onClick={() => navigate("/game")}>
          PLAY
        </button>
        <button className="btn" onClick={() => navigate("/tutorial")}>
          TUTORIAL
        </button>
        <button
          className="btn"
          disabled={!hasSave}
          onClick={() => navigate("/game?resume=1")}
        >
          CONTINUE
        </button>
      </div>
    </main>
  );
}
