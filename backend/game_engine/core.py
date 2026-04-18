"""
Core game engine — state initialization, turn lifecycle, and player actions.
All math aligned to architecture.md config constants.
"""
import random
from sqlalchemy.orm import Session
from backend.models.core import GameState, Player, Property
from backend.config import BALANCE


# ──────────────────────────────────────────────
#  PROPERTY BLUEPRINTS (10 total, matching sprites)
# ──────────────────────────────────────────────
BLUEPRINTS = [
    {"name": "Startup Lofts",  "key": "startup_lofts",  "tier": "budget",  "val": 6_000,  "unlock": 1},
    {"name": "Trade Center",   "key": "trade_center",   "tier": "budget",  "val": 7_000,  "unlock": 5},
    {"name": "Signal Tower",   "key": "signal_tower",   "tier": "budget",  "val": 8_000,  "unlock": 1},
    {"name": "Market Block",   "key": "market_block",   "tier": "budget",  "val": 9_000,  "unlock": 18},
    {"name": "Venture Place",  "key": "venture_place",  "tier": "mid",     "val": 12_000, "unlock": 1},
    {"name": "Capital Square", "key": "capital_square",  "tier": "mid",     "val": 14_000, "unlock": 3},
    {"name": "Exchange Tower", "key": "exchange_tower",  "tier": "mid",     "val": 16_000, "unlock": 7},
    {"name": "Metro Spire",    "key": "metro_spire",    "tier": "mid",     "val": 18_000, "unlock": 12},
    {"name": "Mogul Tower",    "key": "mogul_tower",    "tier": "premium", "val": 28_000, "unlock": 9},
    {"name": "Apex Plaza",     "key": "apex_plaza",     "tier": "premium", "val": 38_000, "unlock": 15},
]


def _calc_rent(base_value: int, dev_level: int = 0) -> int:
    """Rent = base_value × BASE_RENT_YIELD × dev_multiplier."""
    return int(base_value * BALANCE.BASE_RENT_YIELD * BALANCE.rent_multiplier(dev_level))


def _calc_dev_cost(market_value: int) -> int:
    """Dev cost = FLAT_FEE + PERCENT_FEE × market_value."""
    return int(BALANCE.DEV_FLAT_FEE + BALANCE.DEV_PERCENT_FEE * market_value)


def _calc_net_worth(db: Session, player: Player) -> int:
    """Net worth = cash + sum(market_value × dev_value_mult) - debt."""
    props = db.query(Property).filter(Property.owner_id == player.id).all()
    portfolio = sum(
        int(p.market_value * BALANCE.dev_value_multiplier(p.dev_level))
        for p in props
    )
    return player.cash + portfolio - player.debt


# ──────────────────────────────────────────────
#  GAME INIT
# ──────────────────────────────────────────────

def create_new_game(db: Session, session_id: str) -> GameState:
    """Initializes a new game: players + 10 property plots."""

    # Wipe any existing session
    db.query(Property).filter(Property.game_id == session_id).delete()
    db.query(Player).filter(Player.game_id == session_id).delete()
    db.query(GameState).filter(GameState.id == session_id).delete()

    game = GameState(
        id=session_id,
        turn=1,
        max_turns=BALANCE.MAX_TURNS,
        current_ap=0,
    )
    db.add(game)

    # Players
    user = Player(
        id=f"{session_id}_user",
        game_id=session_id,
        role="USER",
        cash=BALANCE.STARTING_CASH,
    )
    flipper = Player(
        id=f"{session_id}_flipper",
        game_id=session_id,
        role="FLIPPER",
        cash=BALANCE.STARTING_CASH * 2,
    )
    db.add_all([user, flipper])

    # Properties
    for bp in BLUEPRINTS:
        prop = Property(
            id=f"{session_id}_{bp['key']}",
            game_id=session_id,
            name=bp["name"],
            district="pixel_park",
            tier=bp["tier"],
            sprite_key=bp["key"],
            base_value=bp["val"],
            market_value=bp["val"],
            rent_value=_calc_rent(bp["val"], 0),
            dev_level=0,
            tenant_bonus=1.0,
            is_listed=False,
            unlock_turn=bp["unlock"],
        )
        db.add(prop)

    db.commit()
    return game


# ──────────────────────────────────────────────
#  TURN LIFECYCLE
# ──────────────────────────────────────────────

def start_turn(db: Session, game: GameState) -> dict:
    """
    Start-of-turn sequence (architecture.md §2):
      1. Pay mortgage/debt interest
      2. Drip-feed property listings
      3. Roll AP (1d4+1)
    Returns dict with ap, low_roll flag, and newly listed property ids.
    """
    newly_listed = []

    # 1. Debt interest (deducted from cash at START of turn)
    for p in db.query(Player).filter(Player.game_id == game.id).all():
        if p.debt > 0 and not p.is_bankrupt:
            interest = int(p.debt * BALANCE.MORTGAGE_INTEREST_RATE)
            p.cash -= interest

    # 2. Drip-feed property listings
    props = db.query(Property).filter(
        Property.game_id == game.id,
        Property.unlock_turn <= game.turn,
        Property.is_listed == False,
        Property.owner_id == None,
        Property.expiry_turn == None,  # hasn't already expired once
    ).all()
    for prop in props:
        prop.is_listed = True
        prop.expiry_turn = game.turn + BALANCE.PROPERTY_EXPIRY_TURNS
        newly_listed.append(prop.id)

    # 3. Roll AP
    rolled_ap = random.randint(1, BALANCE.AP_DICE_SIDES) + BALANCE.AP_DICE_MODIFIER
    game.current_ap = rolled_ap
    is_low_roll = rolled_ap <= BALANCE.LOW_ROLL_THRESHOLD

    db.commit()
    return {
        "ap": rolled_ap,
        "low_roll": is_low_roll,
        "newly_listed": newly_listed,
        "turn": game.turn,
    }


def end_turn(db: Session, game: GameState) -> dict:
    """
    End-of-turn sequence (architecture.md §2):
      1. Collect rent for all owned properties
      2. Expire old listings
      3. Check bankruptcy / victory
      4. Advance turn counter
    Returns dict with summary info.
    """
    user = db.query(Player).filter(
        Player.game_id == game.id, Player.role == "USER"
    ).first()

    # 1. Rent collection
    total_rent = 0
    owned = db.query(Property).filter(
        Property.game_id == game.id,
        Property.owner_id != None,
    ).all()
    for prop in owned:
        owner = db.query(Player).filter(Player.id == prop.owner_id).first()
        if owner and not owner.is_bankrupt:
            owner.cash += prop.rent_value
            if owner.id == user.id:
                total_rent += prop.rent_value

    # 2. Expire old listings (unowned past their expiry turn)
    expired_ids = []
    expired = db.query(Property).filter(
        Property.game_id == game.id,
        Property.is_listed == True,
        Property.owner_id == None,
        Property.expiry_turn != None,
        Property.expiry_turn <= game.turn,
    ).all()
    for prop in expired:
        prop.is_listed = False
        prop.market_value = int(prop.market_value * 0.9)
        expired_ids.append(prop.id)

    # 3. Victory / bankruptcy checks
    game_over = False
    victory = False
    net_worth = _calc_net_worth(db, user) if user else 0
    user_props_count = db.query(Property).filter(Property.owner_id == user.id).count() if user else 0

    if (
        game.turn >= BALANCE.EARLY_WIN_TURN
        and net_worth >= BALANCE.EARLY_WIN_NET_WORTH
        and user_props_count >= BALANCE.EARLY_WIN_MIN_PROPERTIES
    ):
        game_over = True
        victory = True

    # Bankruptcy check (LTV based)
    if user and user.debt > 0:
        portfolio_val = max(net_worth + user.debt - user.cash, 1)
        ltv = user.debt / portfolio_val
        if ltv >= BALANCE.BANKRUPTCY_LTV:
            user.is_bankrupt = True
            game_over = True

    # 4. Advance turn
    if game.turn >= game.max_turns:
        game_over = True
    else:
        game.turn += 1
        game.current_ap = 0

    db.commit()
    return {
        "turn": game.turn,
        "rent_collected": total_rent,
        "expired": expired_ids,
        "net_worth": net_worth,
        "game_over": game_over,
        "victory": victory,
    }


# ──────────────────────────────────────────────
#  PLAYER ACTIONS (each costs 1 AP)
# ──────────────────────────────────────────────

def buy_property(db: Session, game: GameState, player: Player, property_id: str) -> dict:
    """
    Buy action (1 AP):
      - Property must be listed and unowned
      - Player must have enough cash
      - Deducts cash, assigns ownership, delists
    """
    if game.current_ap < 1:
        return {"success": False, "error": "Not enough AP (need 1)"}

    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        return {"success": False, "error": "Property not found"}
    if not prop.is_listed:
        return {"success": False, "error": "Property is not currently listed"}
    if prop.owner_id is not None:
        return {"success": False, "error": "Property is already owned"}
    if player.cash < prop.market_value:
        return {"success": False, "error": f"Not enough cash (need ${prop.market_value:,}, have ${player.cash:,})"}

    # Execute purchase
    player.cash -= prop.market_value
    prop.owner_id = player.id
    prop.is_listed = False
    prop.expiry_turn = None
    game.current_ap -= 1

    db.commit()
    return {
        "success": True,
        "property": prop.name,
        "cost": prop.market_value,
        "cash_remaining": player.cash,
        "ap_remaining": game.current_ap,
    }


def develop_property(db: Session, game: GameState, player: Player, property_id: str) -> dict:
    """
    Develop action (1 AP):
      - Must own the property
      - Dev level must be < MAX_DEV_LEVEL (3)
      - Cost = $500 + 15% × market_value
      - Increases dev_level, recalculates rent and market value
    """
    if game.current_ap < 1:
        return {"success": False, "error": "Not enough AP (need 1)"}

    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        return {"success": False, "error": "Property not found"}
    if prop.owner_id != player.id:
        return {"success": False, "error": "You don't own this property"}
    if prop.dev_level >= BALANCE.MAX_DEV_LEVEL:
        return {"success": False, "error": "Property already at max development (level 3)"}

    cost = _calc_dev_cost(prop.market_value)
    if player.cash < cost:
        return {"success": False, "error": f"Not enough cash (need ${cost:,}, have ${player.cash:,})"}

    # Execute development
    player.cash -= cost
    prop.dev_level += 1
    prop.rent_value = _calc_rent(prop.base_value, prop.dev_level)
    prop.market_value = int(prop.base_value * BALANCE.dev_value_multiplier(prop.dev_level))
    game.current_ap -= 1

    db.commit()
    return {
        "success": True,
        "property": prop.name,
        "new_level": prop.dev_level,
        "cost": cost,
        "new_rent": prop.rent_value,
        "new_market_value": prop.market_value,
        "cash_remaining": player.cash,
        "ap_remaining": game.current_ap,
    }


def research_action(db: Session, game: GameState, player: Player, property_id: str) -> dict:
    """
    Research action (1 AP):
      - Reveals intel about a property or upcoming catalyst
      - Full trivia engine is Phase 5; this is a working stub
    """
    if game.current_ap < 1:
        return {"success": False, "error": "Not enough AP (need 1)"}

    prop = db.query(Property).filter(Property.id == property_id).first()
    if not prop:
        return {"success": False, "error": "Property not found"}

    game.current_ap -= 1
    db.commit()

    # Stub: return basic property intel
    return {
        "success": True,
        "property": prop.name,
        "intel": {
            "base_value": prop.base_value,
            "market_value": prop.market_value,
            "rent_per_turn": prop.rent_value,
            "dev_level": prop.dev_level,
            "tier": prop.tier,
            "hint": "The trivia engine will replace this stub in Phase 5.",
        },
        "ap_remaining": game.current_ap,
    }
