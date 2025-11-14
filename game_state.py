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
    
    if player.money <= 0 and st.session_state.mafia_active:
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
