"""Game state management using Streamlit session state."""
import streamlit as st
from player import Player

def initialize_game_state():
    """Initialize all session state variables."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.player = Player()
        st.session_state.current_page = "main_menu"
        st.session_state.mafia_active = False
        st.session_state.mafia_event_pending = False
        st.session_state.mafia_demand_amount = 0
        st.session_state.game_over = False
        st.session_state.game_over_reason = ""
        st.session_state.inventory = []
        st.session_state.sound_enabled = True
        
        # Casino game states
        st.session_state.casino_game = None
        st.session_state.blackjack_state = {}
        st.session_state.roulette_state = {}
        st.session_state.dice_state = {}
        st.session_state.horse_state = {}
        
        # Flag to track if a significant action was performed (for mafia event triggering)
        st.session_state.significant_action_performed = False

    # Defaults also migrate sessions started before social features were added.
    defaults = {
        "mafia_event_pending": False, "mafia_demand_amount": 0,
        "significant_action_performed": False,
        "blackjack_state": {}, "roulette_state": {},
        "social_unlocked": False, "social_requests": [], "social_contacts": [],
        "social_next_id": 1, "social_last_action": 0, "social_raids": [],
        "mafia_groups": [
            {"id": "karahan", "name": "Karahan Ailesi", "total": 24},
            {"id": "kuzgun", "name": "Kuzgunlar", "total": 18},
            {"id": "liman", "name": "Liman Kardeşliği", "total": 30},
        ],
        "mafia_event_group": None, "mafia_event_source": "normal",
        "normal_mafia_queued": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def navigate_to(page):
    """Navigate to a different page."""
    st.session_state.current_page = page
    st.rerun()

def get_player():
    """Get the current player object."""
    return st.session_state.player

def check_death_conditions():
    """Check if player should die."""
    player = get_player()
    
    if not player.is_alive():
        st.session_state.game_over = True
        st.session_state.game_over_reason = "Your HP reached 0. You died."
        return True
    
    # Blackjack stakes are held by the table until every hand is settled.
    blackjack = st.session_state.get("blackjack_state", {})
    money_on_table = blackjack.get("active") and not blackjack.get("settled")
    if player.money <= 0 and st.session_state.mafia_active and not money_on_table:
        st.session_state.game_over = True
        st.session_state.game_over_reason = "You ran out of money. The mafia killed you."
        return True
    
    return False

def activate_mafia_if_needed():
    """Activate mafia when player reaches $10,000."""
    player = get_player()
    if not st.session_state.mafia_active and player.money >= 10000:
        st.session_state.mafia_active = True
        return True
    return False

def mark_significant_action():
    """Mark that a significant action was performed (triggers mafia check)."""
    st.session_state.significant_action_performed = True
