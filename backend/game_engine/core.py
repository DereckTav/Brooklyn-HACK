import uuid
import random
from sqlalchemy.orm import Session
from backend.models.core import GameState, Player, Property
import backend.config as config

def create_new_game(db: Session, session_id: str) -> GameState:
    """Initializes a new game state, creating players and 10 property plots."""
    
    # Delete existing game for this session to reset
    db.query(Property).filter(Property.game_id == session_id).delete()
    db.query(Player).filter(Player.game_id == session_id).delete()
    db.query(GameState).filter(GameState.id == session_id).delete()
    
    # Core state
    game = GameState(id=session_id, turn=1, max_turns=config.MAX_TURNS, current_ap=0)
    db.add(game)
    
    # Create Players
    user = Player(
        id=f"{session_id}_user", 
        game_id=session_id, 
        role="USER", 
        cash=config.STARTING_CASH
    )
    flipper = Player(
        id=f"{session_id}_flipper", 
        game_id=session_id, 
        role="FLIPPER", 
        cash=int(config.STARTING_CASH * 2.0) # Flipper gets rich start
    )
    db.add_all([user, flipper])
    
    # Property Blueprints (Matching sprite_registry.json)
    blueprints = [
        {"name": "Startup Lofts", "tier": "budget", "val": 6000},
        {"name": "Trade Center", "tier": "budget", "val": 7000},
        {"name": "Signal Tower", "tier": "budget", "val": 8000},
        {"name": "Market Block", "tier": "budget", "val": 9000},
        {"name": "Venture Place", "tier": "mid", "val": 12000},
        {"name": "Capital Square", "tier": "mid", "val": 14000},
        {"name": "Exchange Tower", "tier": "mid", "val": 16000},
        {"name": "Metro Spire", "tier": "mid", "val": 18000},
        {"name": "Mogul Tower", "tier": "premium", "val": 28000},
        {"name": "Apex Plaza", "tier": "premium", "val": 38000},
    ]
    
    # Populate properties
    for bp in blueprints:
        prop = Property(
            id=f"{session_id}_{bp['name'].replace(' ', '_').lower()}",
            game_id=session_id,
            name=bp['name'],
            district="pixel_park",
            tier=bp['tier'],
            base_value=bp['val'],
            market_value=bp['val'],
            rent_value=int(bp['val'] * config.BASE_RENT_MULTIPLIER_BUDGET if bp['tier'] == "budget" else bp['val'] * 0.15)
        )
        db.add(prop)
        
    db.commit()
    return game

def start_turn(db: Session, game: GameState) -> int:
    """
    Rolls 1d4+1 AP (Action Points).
    Applies property expiries before the round begins.
    Returns the rolled AP amount.
    """
    # Expiry Check
    expired_props = db.query(Property).filter(
        Property.game_id == game.id,
        Property.is_listed == True,
        Property.expiry_turn <= game.turn
    ).all()
    
    for prop in expired_props:
        prop.is_listed = False
        prop.expiry_turn = None
        # Drop value by 10% on expiry
        prop.market_value = int(prop.market_value * 0.9)
        
    # Roll AP
    rolled_ap = random.randint(1, 4) + 1  # 2 to 5 AP
    game.current_ap = rolled_ap
    
    db.commit()
    return rolled_ap

def end_turn(db: Session, game: GameState):
    """
    Ends the current turn, processing all cash flow (Rent & Debt).
    Moves the game state forward to the next round.
    """
    # 1. Cash Flow: Collect Rent for all owned properties
    owned_properties = db.query(Property).filter(
        Property.game_id == game.id,
        Property.owner_id != None
    ).all()
    
    for prop in owned_properties:
        owner = db.query(Player).filter(Player.id == prop.owner_id).first()
        if owner and not owner.is_bankrupt:
            # Add rent income to owner's cash
            # Rate is stored in prop.rent_value (dynamically shifts via catalysts later)
            owner.cash += prop.rent_value
            
    # 2. Debt Math: Apply 5% interest per turn on any outstanding debt
    players = db.query(Player).filter(Player.game_id == game.id).all()
    for p in players:
        if p.debt > 0 and not p.is_bankrupt:
            # 5% interest per turn (simulating high tension leverage)
            interest = int(p.debt * 0.05)
            p.debt += interest
            
            # Check bankruptcy condition if cash < 0 and debt ratio is terrible (Tier 2 rules)
            if p.cash < 0:
                p.is_bankrupt = True
    
    # 3. Advance Turn State
    if game.turn >= game.max_turns:
        # Game over state triggered
        pass
    else:
        game.turn += 1
        game.current_ap = 0 # AP resets
        
    db.commit()
