import type { GridPos, Property } from "../types/game";
import { useGameStore } from "../store/gameStore";

const TILE_W = 128;
const ROW_STAGGER_X = 64;
const ROW_Y = 56;

interface Props {
  property: Property;
  position: GridPos;
  unlocked: boolean;
}

export default function PropertyTile({ property, position, unlocked }: Props) {
  const selectedId = useGameStore((s) => s.selectedPropertyId);
  const selectProperty = useGameStore((s) => s.selectProperty);
  const ownedIds = useGameStore((s) => s.ownedPropertyIds);
  const listedIds = useGameStore((s) => s.listedPropertyIds);

  const isSelected = selectedId === property.id;
  const isOwned = ownedIds.includes(property.id);
  const isListed = listedIds.includes(property.id);

  const baseX = position.row === 1 ? 0 : ROW_STAGGER_X;
  const x = baseX + position.col * TILE_W;
  const y = position.row * ROW_Y;
  const z = isSelected ? 200 : position.row * 10 + position.col;

  const handleClick = () => {
    if (!unlocked) return;
    selectProperty(isSelected ? null : property.id);
  };

  let tileClass = "tile";
  if (!unlocked) tileClass += " tile--locked";
  if (isSelected) tileClass += " tile--selected";
  if (isOwned) tileClass += " tile--owned";

  return (
    <button
      type="button"
      className={tileClass}
      style={{ left: x, top: y, zIndex: z }}
      title={`${property.name} — $${property.baseValue.toLocaleString()}${isOwned ? " (OWNED)" : isListed ? " (AVAILABLE)" : ""}`}
      disabled={!unlocked}
      onClick={handleClick}
    >
      <div className="tile__shadow" />
      <div className="tile__base" />
      <img src={property.sprite} alt={property.name} className="tile__sprite" />
      <span className="tile__tier">{isOwned ? "OWNED" : property.tier}</span>
    </button>
  );
}
