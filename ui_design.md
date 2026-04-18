# Mogul Blocks — UI & Visual Design Document

This document defines the exact layout, color palette, typography, and text copy for the Mogul Blocks frontend. This serves as the master reference for the React/CSS implementation.

---

## 1. Visual Language & Typography

**Vibe:** Cyberpunk-retro / "Corporate Dystopia Pixel Art"
- **Typography:** `Press Start 2P` (Google Fonts) for headers and numbers, `VT323` (Google Fonts) for body text and tooltips to ensure readability at smaller sizes.
- **Borders:** 2px solid, sharp edges (no `border-radius`), often with contrasting border colors.
- **Backgrounds:** Flat colors with subtle noise overlays (CSS `url('data:image...')`) or repetitive scanline gradients.

### Color Palette

| Token | Hex | Usage |
|---|---|---|
| `--color-bg-deep` | `#111115` | Main document background, space behind the board |
| `--color-panel-bg` | `#1E1E24` | Background for UI panels (Player Card, Action Panel) |
| `--color-panel-border`| `#3F3F5A` | Standard border for UI panels |
| `--color-text-main` | `#E0E0E5` | Primary body text |
| `--color-text-muted`| `#8B8B9A` | Secondary text, inactive states |
| `--color-gold` | `#FFD700` | Stars, Player Cash, "YOU" highlighting |
| `--color-orange` | `#E56B30` | Flipper highlighting, alerts, warning states |
| `--color-neon-blue` | `#2D9CDB` | Action buttons (Buy/Develop), positive changes |
| `--color-neon-green`| `#27AE60` | Rent income popups, Boom events |
| `--color-danger` | `#E74C3C` | Debt/Bankruptcy warnings, Bust events |

---

## 2. Screen Wireframes

### Main Game Screen Layout (16:9 Desktop Target)

The screen is divided into 3 main columns: Left Sidebar (Player), Middle (Board), Right Sidebar (Rival & Actions).

```text
+-----------------------------------------------------------------------------------+
|  [TOP BAR] Turn 4/20 | AP: 3 (Dice: *icon*) | Next Unlock: Turn 5      [PAUSE]  |
+-------------------+-------------------------------------------+-------------------+
|  [LEFT PANEL]     |               [GAME BOARD]                |  [RIGHT PANEL]    |
|                   |                                           |                   |
|  == YOU ==        |            [ Isometric Grid ]             |  == FLIPPER ==    |
|  $15,000          |                                           |                   |
|  Props: 2         |           /▔▔▔\        /▔▔▔\              |  Est. Cash:       |
|  Net Worth: a$32K |          /     \      /     \             |  $45,000          |
|                   |          \     /      \     /             |  Props: 3         |
|  [Debt: $0]       |           \___/        \___/              |                   |
|                   |                   ...                     |  [Portrait Image] |
|                   |                                           |                   |
|  == TRASH TALK == |                                           |  == ACTIONS ==    |
|                   |         [ Selected Tile Details ]         |                   |
| > Flipper bought  |         -------------------------         |  [ BUY $8,000 ]   |
|   Signal Tower    |         Startup Lofts (Budget)            |  [ RESEARCH $2K]  |
| > You: "Back off" |         Owner: YOU | Base Rent: $1k       |                   |
|                   |         Level: [*] [*] [ ]                |  [ END TURN ]     |
| [Say something]   |                                           |                   |
+-------------------+-------------------------------------------+-------------------+
|  [INTEL FEED] > Turn 3 catalyst: "Interest rates cut!" Rent +20%                  |
+-----------------------------------------------------------------------------------+
```

### Component Details

**1. Top Bar (`<TopBar />`)**
- Sticky at the top, 40px height. Border-bottom: 2px solid `--color-panel-border`.
- **Left:** Turn counter (`Turn X / 20`). Pulses red on turn 15+.
- **Center:** Action Points (`AP: X`). 
- **Right:** Pause button. `[ || ]`

**2. Player Card / Left Panel (`<PlayerCard />`)**
- 25% width. Stick to left.
- Highlights: Cash uses `--color-gold`. If Debt > 0, show `[Debt: $X]` in `--color-danger`.
- Trash Talk board sits below player stats. A scrollable log of text.

**3. Game Board / Middle Column (`<DistrictBoard />`)**
- 50% width. Dark background (`--color-bg-deep`).
- Contains the 10 property SVGs mapped over the `board_bg.svg`.
- 3-4-3 staggered isometric diamond grid. All 10 tiles visible from turn 1.
- Selected property card floats at the bottom of this column when a property is clicked.

**3a. Property Tile (`<PropertyTile />`)**
Each tile is a pixel-art SVG building. Tiles support the following overlays:
- **Locked state:** Tile renders with CSS `filter: grayscale(1) opacity(0.5)` and is not clickable. When a tile unlocks, it animates from grayscale to full color with a scale pop (`transform: scale(1.1) → 1.0`, 0.3s).
- **Flipper target indicator:** When the Flipper AI has flagged this tile as a buy target, a `👀` icon renders in the **top-right corner** of the tile (12x12px, `--color-orange` background badge). The icon has a subtle 2s pulse animation to draw the eye.
- **Expiry countdown badge:** When a listed property has ≤5 turns before expiring, a small numeric badge renders in the **top-left corner** showing turns remaining (5 → 4 → 3 → 2 → 1). Badge is `--color-danger` when at 2 or below.
- **Ownership border:** Owned properties get a 2px border in `--color-gold` (YOU) or `--color-orange` (Flipper).
- **Development level:** Stars overlay at the bottom-center — up to 3 stars (`[*] [*] [*]`) in `--color-gold`.

**4. Rival Card & Actions / Right Panel (`<RivalCard />`, `<ActionPanel />`)**
- 25% width. Stick to right.
- Shows `<img src="sprites/flipper.svg">`. Est Cash uses `--color-orange`.
- Main interaction buttons are chunky, pixel-art style buttons at the bottom.
- **MVP v1 buttons:** `BUY`, `RESEARCH`, `END TURN`.
- **v2 button:** `DEVELOP` — reserves its slot in the panel but is hidden/disabled in MVP.

**5. Dice Roll Modal (`<DiceModal />`)**
- Appears at the start of every turn, blocking the UI until rolled.
- Central pixel-art dice icon. User clicks "ROLL".
- Evaluates `1d4+1` (resulting in 2-5).
- Plays CSS 3D tumble animation (`@keyframes spin`), then lands on the result.
- Displays "+X Action Points" and fades out, passing the AP to the Top Bar.

---

## 3. UI Copy & Text References

Consistency in phrasing helps the player learn the game mechanics quickly.

**Action Buttons:**
- Disabled state text: `NOT ENOUGH AP` or `NOT ENOUGH CASH` or `MAX LEVEL`
- Regular state: `BUY ($X)` / `DEVELOP ($X)` / `RESEARCH ($X)`
- End Turn: `END TURN (X AP Left)` — Pulses if player taps end turn with unused AP.

**Trash Talk (Pre-made options for MVP):**
Before taking action, the player can optionally select a message to Flipper from a dropdown:
- *"I'm taking over this block."* (Aggressive)
- *"You don't have the cash for that."* (Bluff)
- *"Looking to sell?"* (Misdirection)

**Events & Notifications (`<EventToast />`):**
Toast notifications slide in from the top-right.
- New Listing: *"New listing available: {Property Name}!"*
- Flipper Buy: *"Flipper snapped up {Property Name}!"*
- Rent Received: *"+${Amount} Rent Collected"*

**Bankruptcy States:**
- Warning (80% LTV): `"WARNING: High Debt to Asset Ratio. Liquidations imminent."`
- Bankrupt: `"LIQUIDATED. Flipper bought out your debts."`

**Trivia Modals (`<TriviaModal />`):**
Trivia fires in three contexts. All use the same modal component with a semi-transparent gray overlay, but with a different header color and copy to signal the context to the player.

| Context | Header | Header Color | Trigger |
|---|---|---|---|
| Catalyst event | `MARKET SHIFT DETECTED` | `--color-neon-green` | Automatic, between turns |
| Research action | `MARKET RESEARCH` | `--color-neon-blue` | Player spends AP on Research |
| 2-AP penalty | `LOW ROLL — STAY SHARP` | `--color-orange` | Automatic on any turn where dice rolls 2 AP |

Shared modal structure:
- Body: `[Trivia Question Text]`
- Footer buttons: `[ Choice A ]` `[ Choice B ]` `[ Choice C ]`

Context-specific result copy:
- **Catalyst success:** `"Correct! Market confidence high. Boom applied: +20% Rent."`
- **Catalyst failure:** `"Incorrect. Investors are spooked. Bust applied: -15% Property Value."`
- **Research success:** `"Intel acquired: [catalyst hint revealed]"`
- **Research failure:** `"Bad intel. Misleading tip added to feed."`
- **Penalty success:** `"Crisis averted. Proceeding with 2 AP."`
- **Penalty failure:** `"-$1,000. Proceeding with 2 AP."`

---

## 4. Animation Timings (CSS references)

- **Tile selection:** Immediate 1px border shift to white.
- **Button hover:** `transform: translateY(-2px); box-shadow: 2px 2px 0 var(--color-neon-blue);` transition 0.1s.
- **Toast slide:** `0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275)` for bouncy pixel effect.
- **Cash Danger Mode:** When player cash drops below one full turn of rent income, the outer screen `<body>` gets a pulsing 4px inner border in `--color-danger`. Animation: `@keyframes danger-pulse` at 1.5s ease-in-out infinite, alternating between `box-shadow: inset 0 0 0 4px rgba(231, 76, 60, 0.8)` and `inset 0 0 0 4px rgba(231, 76, 60, 0.2)`. Clears immediately once cash rises above the threshold.
- **Tile unlock:** Scale pop `1.1 → 1.0` over 0.3s paired with filter transition from grayscale to full color.
- **Flipper eyes pulse:** 2s ease-in-out infinite opacity cycle from 1.0 → 0.6 → 1.0 to keep the indicator eye-catching without being noisy.
