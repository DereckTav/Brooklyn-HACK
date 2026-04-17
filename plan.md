# Mogul Blocks — Game Design Plan

## One-Liner

A single-player real estate tycoon web game where pop culture knowledge is your competitive edge, and finance concepts are taught through mechanics — never lectures.

---

## Core Loop

Research the market → Anticipate catalysts → Position your capital → Collect returns → Reinvest.

Every turn, the player allocates **3 Action Points (AP)** across six possible actions. Limited AP forces constant tradeoffs, mirroring real capital allocation.

---

## Turn Structure

Each game runs **20 turns**. A full session takes roughly 15-20 minutes.

### Action Menu

| Action | AP Cost | What It Does |
|---|---|---|
| Buy | 1 | Purchase an available property. Triggers sealed-bid auction if an AI rival also wants it. |
| Develop | 1 | Upgrade a property you own (add floors, renovate, add amenities). Increases rent yield but costs cash. |
| Bid | 2 | Compete for a premium tenant or anchor brand. Winning locks in boosted rent for several turns. |
| Trade | 1 | Propose a swap or sale to an AI rival. Rival evaluates based on personality and your reputation. |
| Research | 1 | Answer a trivia question to reveal hidden upcoming market catalysts. Wrong answers return misleading intel. |
| Sabotage | 2 | Disrupt a rival: plant a bad review (lowers their rent), lobby for rezoning, or poach their tenant. |

### Why 3 AP Works

Players can never do everything in a single turn. Buy + Research + Develop = 3 AP (full turn spent). Sabotage + Buy = 3 AP (no time left to develop). This forces strategic prioritization every turn with no dead turns.

### Action Chaining (The Killer Loop)

Turn 1: Research (trivia reveals "Tech district boom in 2 turns")
Turn 2: Buy cheap in the tech district before price moves
Turn 3: Develop the property as the catalyst hits and rent spikes

A player who skipped research only sees the boom after it happens and reacts late. This mirrors how research-driven investing actually works.

---

## Information Asymmetry System (Trivia Integration)

Trivia is not a side minigame. It is the primary source of competitive advantage.

### Hidden Event Queue

Each game generates a queue of 3-5 upcoming catalyst events scheduled for future turns. Players cannot see them by default. Spending AP on Research (trivia) peels back the curtain.

### Trivia Difficulty Tiers

- **Easy question** — Reveals the district affected ("Something is happening in the Fashion district soon")
- **Medium question** — Reveals the direction ("Fashion district rents will increase")
- **Hard question** — Reveals magnitude and timing ("Fashion district +45% rent in 2 turns due to a celebrity flagship store opening")

### Wrong Answers

Wrong answers do not return nothing. They return **bad intel** — misleading information that could cause the player to misallocate capital. This creates real risk in the research action, mirroring how real due diligence can lead to incorrect conclusions.

### Content Sustainability

Events are generated from templates:

```
[Celebrity / Brand / Trend] + [moves into / leaves / boycotts] + [District] = [Rent effect]
```

50 templates generate thousands of unique combinations. Handcrafted trivia questions are reserved for rare "Insider Tip" events that give outsized alpha.

---

## AI Rival Archetypes

Four personality types that teach different strategies by opposing the player.

### The Flipper
- Buys cheap, sells at any profit, never develops
- Lesson: Flipping is fast but leaves long-term money on the table

### The Builder
- Buys and develops aggressively, uses heavy leverage
- Dominates in bull markets, gets wiped in downturns
- Lesson: The risk of over-leverage

### The Analyst
- Spends lots of AP on research, makes fewer but better-timed moves
- Lesson: The value of information and patience

### The Shark
- Sabotage-heavy, poaches tenants, plays politics
- Lesson: Defensive portfolio management and factoring in competitive threats

### Difficulty Scaling

- **Easy mode** — AI rivals react to catalysts 1-2 turns late
- **Hard mode** — AI rivals appear to have their own intel sources and move before the player

### Combination Meta

Each game features 2-3 rivals. Different combinations change the strategy required. Flipper + Shark feels very different from Builder + Analyst. This provides replay variety without needing multiplayer.

---

## Skill-Based Mechanics and Game Theory

### Sealed-Bid Auctions

When two players want the same property, both submit a hidden bid. Highest bid wins, but overpaying destroys ROI. Players learn the winner's curse by feeling it — not reading about it.

### Reputation System (Prisoner's Dilemma)

Trade offers to AI rivals can be fair or exploitative. Fair trades build reputation, making future deals easier. Lowball offers might work once, but the AI remembers and stops cooperating. This teaches that repeated games favor cooperation.

### Bluffing and Signaling

Before catalyst events, players can publicly "announce" plans ("I am going to develop heavily in the Sports district"). AI rivals react to announcements. Players can bluff — announce Sports, then buy Fashion while rivals pile into Sports. Teaches strategic misdirection and signaling.

---

## Finance Progression (Hidden Curriculum)

Finance concepts are never introduced as lessons. They are unlocked as tools when the player demonstrates mastery of the prerequisite behavior.

### Tier 1 — Cash Flow Basics (Turns 1-5)
- Buy properties, collect rent, pay expenses
- Player intuitively learns: revenue minus costs equals profit (NOI)
- No jargon on screen

### Tier 2 — Leverage (Unlocks around Turn 10)
- Mortgage option appears: borrow to buy more, but interest eats into cash flow
- Player learns that leverage amplifies both gains and losses
- Downturn events can trigger forced sales if over-leveraged

### Tier 3 — Valuation (Unlocks via skill milestones)
- **Win 3 auctions profitably** → Unlock "Comparable Analysis" (see recent sale prices of similar properties)
- **Survive a downturn without going bankrupt** → Unlock "Stress Testing" (preview portfolio performance under worst-case scenarios)
- **Predict 5 catalysts correctly via trivia** → Unlock "Trend Modeling" (see probability distributions on future events instead of point estimates)
- **Execute a profitable bluff** → Unlock "Market Manipulation" (spend AP to artificially inflate or deflate district hype for 1 turn)

### Tier 4 — Portfolio Management (Late Game / Prestige)
- Combine properties into portfolios
- See aggregate yield, concentration risk, sector exposure
- Unlock "Cap Rate" and "ROI" labels for metrics that were always on screen but unnamed

### Design Principle

The game never says "here is a lesson on comparable analysis." It says "you earned a new power." Labels for real finance concepts appear only after the player already understands the mechanic intuitively.

---

## City and District Design

### District Themes

| District | Culture Angle | Typical Catalysts |
|---|---|---|
| Hollywood | Film, TV, streaming | Blockbuster releases, award seasons, studio deals |
| Beatstreet | Music, concerts, nightlife | Album drops, festival announcements, artist residencies |
| Pixel Park | Gaming, esports, tech | Game launches, tournament hosting, tech company moves |
| Stadium Row | Sports, athletics | Championship runs, team relocations, draft picks |
| Trend Ave | Fashion, streetwear, beauty | Brand collabs, fashion weeks, influencer moves |
| Flavor Town | Food, restaurants, culinary | Chef openings, food trends, review surges |

### District Mechanics

- Each district has a base rent multiplier that shifts with catalysts
- Owning 3+ properties in one district gives a "Monopoly Bonus" (set completion, Monopoly-style)
- Districts can be rezoned via sabotage actions, changing their theme and value profile

---

## MVP Scope (Version 1)

### What Ships

- 1 city, 1 district (Pixel Park — gaming/tech theme), 10 properties
- Single screen, no scrolling map
- 3 AP per turn, 20-turn games
- 1 AI rival (The Flipper)
- 3 action types only: Buy, Develop, Research
- 5 catalyst event templates
- 2 finance tiers: cash flow basics + simple leverage (mortgage unlock at turn 10)
- No accounts, no leaderboards, no multiplayer
- Web-based, single-page React app

### What This Tests

Is the core loop of "research → anticipate → position → profit" fun on its own? If yes, layer in the remaining systems. If no, rework before building more.

### MVP Success Criteria

- Playtesters complete at least 3 full games without prompting
- Players can articulate (without being told) why research gave them an edge
- Average session length exceeds 10 minutes
- Players express desire for more districts, rivals, or actions

---

## Post-MVP Roadmap

### Phase 2 — Depth
- Add remaining 5 districts
- Add Trade and Sabotage actions
- Add 3 remaining AI archetypes (Builder, Analyst, Shark)
- Expand to 15 catalyst templates
- Unlock Tier 3 finance tools (comps, stress testing, trend modeling)

### Phase 3 — Social
- Multiplayer mode (2-4 players, async turn-based)
- Leaderboards (highest portfolio value, best ROI, longest win streak)
- Replay sharing (export a game as a shareable recap)

### Phase 4 — Meta
- Prestige system (restart with cosmetic unlocks and harder AI)
- Community-submitted trivia questions with voting/validation
- Seasonal content (real-world cultural events reflected in game catalysts)
- Mobile optimization

---

## Competitive Positioning

### The Gap

| Competitor | What It Does | What It Lacks |
|---|---|---|
| Monopoly GO | Gambling dopamine, board game skin | No skill, no learning, no strategy |
| Landlord Tycoon | Real-world map, property clicker | No strategic depth |
| Cashflow (Kiyosaki) | Educational board game | Dry, dated, no entertainment hook |
| Wall Street Survivor | Stock market simulator | No real estate, no culture layer |

### Mogul Blocks' Unique Angle

"The game that accidentally teaches you to think like an investor."

The only game where pop culture knowledge IS the alpha. No competitor connects "knowing which anime is trending" to "making a better investment decision."

### Target Audience

Young, culturally plugged-in people (18-28) who are curious about finance but will not sit through a course. They consume content on TikTok, Twitter/X, and YouTube. They play casual strategy games. They want to feel smart, not lectured.

### Distribution Strategy

- Host MVP on personal domain or itch.io
- Post gameplay clips on TikTok and Twitter/X showing "aha" moments (player spots catalyst, positions early, watches AI rivals panic)
- Finance Twitter and gaming Twitter rarely overlap — this lives in both feeds
- No marketing budget needed for validation. Organic shareability is the test.

---

## Technical Stack (Recommended)

- **Frontend**: React (single-page app, component-based UI)
- **Styling**: Tailwind CSS
- **State management**: React useState/useReducer (no external state library needed for MVP)
- **AI rival logic**: Simple decision trees, no ML needed
- **Trivia/catalyst engine**: JSON template system with randomization
- **Hosting**: Vercel or Netlify (free tier sufficient for MVP)
- **No backend needed for MVP** — all game logic runs client-side

---

## Open Questions

1. Should turn count be fixed (20) or should games end when a player hits a net worth target?
2. Should properties have visual upgrades (sprites change when developed) or is text/number UI sufficient for MVP?
3. How punishing should downturns be? Bankruptcy = game over, or just a setback?
4. Should the bluffing mechanic exist in single-player, or is it only meaningful against human opponents?
5. What is the right ratio of skill (trivia, auction strategy) vs. randomness (catalyst timing, property availability)?
