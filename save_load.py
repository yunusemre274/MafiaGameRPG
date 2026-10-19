"""Save and load system using JSON."""
import json
import streamlit as st
from game_state import get_player
from inventory import InventoryItem

SAVE_FILE = "savegame.json"
PERSISTENT_KEYS = [
    "social_unlocked", "social_requests", "social_contacts", "social_next_id",
    "social_last_action", "social_raids", "mafia_groups", "mafia_event_group",
    "mafia_event_source", "mafia_event_pending", "mafia_demand_amount",
    "normal_mafia_queued", "significant_action_performed",
]

def save_game():
    """Save the current game state to JSON."""
    player = get_player()
    
    save_data = {
        "version": 2,
        "world": {key: st.session_state[key] for key in PERSISTENT_KEYS},
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
        
        # Clear transient hands/results so loading cannot replay an old payout.
        for key in list(st.session_state.keys()):
            if key.startswith(('bj_', 'roulette_', 'dice_', 'coin_', 'race_', 'cm_', 'mc_', 'pm_', 'cb_', 'ng_')):
                del st.session_state[key]
        st.session_state.blackjack_state = {}
        st.session_state.current_minigame = None
        st.session_state.game_over = False
        st.session_state.game_over_reason = ''
        from game_state import initialize_game_state
        for key in PERSISTENT_KEYS:
            st.session_state.pop(key, None)
        initialize_game_state()
        for key, value in save_data.get('world', {}).items():
            if key in PERSISTENT_KEYS:
                st.session_state[key] = value

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
        
        if 'world' not in save_data:
            st.session_state.social_last_action = player.total_actions
        return True, "Game loaded successfully!"
    except FileNotFoundError:
        return False, "No save file found."
    except Exception as e:
        return False, f"Error loading game: {str(e)}"
