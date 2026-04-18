import { create } from "zustand";

export type GameView = "launch" | "tutorial" | "game";

interface GameStore {
  view: GameView;
  setView: (view: GameView) => void;
}

export const useGameStore = create<GameStore>((set) => ({
  view: "launch",
  setView: (view) => set({ view }),
}));
