"""Save and load system using JSON."""
import json
import streamlit as st
from game_state import get_player
from inventory import InventoryItem

SAVE_FILE = "savegame.json"

def save_game():
    """Save the current game state to JSON."""
    player = get_player()
    
    save_data = {
        "player": player.to_dict(),
        "inventory": [item.to_dict() for item in st.session_state.inventory],
        "mafia_active": st.session_state.mafia_active,
        "current_page": st.session_state.current_page
    }
    
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True, "Game saved successfully!"
    except Exception as e:
        return False, f"Error saving game: {str(e)}"

def load_game():
    """Load game state from JSON."""
    try:
        with open(SAVE_FILE, 'r') as f:
            save_data = json.load(f)
        
        # Load player data
        player = get_player()
        player.from_dict(save_data["player"])
        
        # Load inventory
        st.session_state.inventory = [
            InventoryItem.from_dict(item_data) 
            for item_data in save_data["inventory"]
        ]
        
        # Load game state
        st.session_state.mafia_active = save_data.get("mafia_active", False)
        st.session_state.current_page = save_data.get("current_page", "main_menu")
        
        return True, "Game loaded successfully!"
    except FileNotFoundError:
        return False, "No save file found."
    except Exception as e:
        return False, f"Error loading game: {str(e)}"
