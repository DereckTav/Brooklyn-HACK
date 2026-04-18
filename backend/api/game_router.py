"""
FastAPI router for core game loop functions.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any

from backend.database import get_db
import backend.game_engine.core as core_engine
from backend.models.core import GameState

router = APIRouter(prefix="/game", tags=["Game"])

@router.post("/start/{session_id}")
def start_game(session_id: str, db: Session = Depends(get_db)):
    """Initializes a new game session and populates the properties."""
    game = core_engine.create_new_game(db, session_id)
    return {"message": "Game started", "session_id": game.id, "turn": game.turn}

@router.post("/{session_id}/turn/start")
def start_turn(session_id: str, db: Session = Depends(get_db)):
    """
    Rolls AP for the current turn.
    Expected to be called once per turn by the frontend before actions are taken.
    """
    game = db.query(GameState).filter(GameState.id == session_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found")
        
    if game.current_ap > 0:
         return {"message": "Already rolled for this turn", "ap": game.current_ap}
         
    rolled_ap = core_engine.start_turn(db, game)
    
    return {
        "message": f"Rolled {rolled_ap} AP",
        "turn": game.turn,
        "ap": rolled_ap
    }

@router.post("/{session_id}/turn/end")
def end_turn(session_id: str, db: Session = Depends(get_db)):
    """
    Ends the current turn, processing all rent collection and debt interest.
    Provides the new turn number back.
    """
    game = db.query(GameState).filter(GameState.id == session_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found")
        
    core_engine.end_turn(db, game)
    
    return {
        "message": "Turn ended, cash flow processed",
        "turn": game.turn
    }

@router.get("/{session_id}/status")
def get_status(session_id: str, db: Session = Depends(get_db)):
    """Returns the current turn, AP, and brief player status."""
    game = db.query(GameState).filter(GameState.id == session_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game session not found")
        
    return {
        "turn": game.turn,
        "ap_remaining": game.current_ap,
        "max_turns": game.max_turns
    }
