"""Roulette casino game."""
import streamlit as st
import random
from game_state import get_player, check_death_conditions, navigate_to
from ui_components import render_section_header, show_success, show_error

def render_roulette():
    """Render the roulette game."""
    render_section_header("Roulette", "🎡")
    
    player = get_player()
    
    # Initialize game state
    if 'roulette_result' not in st.session_state:
        st.session_state.roulette_result = None
        st.session_state.roulette_number = None
    
    st.markdown("### Place Your Bet")
    
    bet_amount = st.number_input(
        "Enter bet amount:",
        min_value=10,
        max_value=player.money,
        value=min(50, player.money),
        step=10,
        key="roulette_bet_input"
    )
    
    bet_type = st.radio(
        "Choose bet type:",
        ["Number (35x)", "Red/Black (2x)", "Even/Odd (2x)"],
        key="roulette_bet_type"
    )
    
    if "Number" in bet_type:
        bet_choice = st.number_input("Pick a number (0-36):", min_value=0, max_value=36, value=0, key="roulette_number")
    elif "Red/Black" in bet_type:
        bet_choice = st.selectbox("Pick a color:", ["Red", "Black"], key="roulette_color")
    else:
        bet_choice = st.selectbox("Pick:", ["Even", "Odd"], key="roulette_even_odd")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎰 Spin Roulette", use_container_width=True):
            result_number = random.randint(0, 36)
            st.session_state.roulette_number = result_number
            
            # Red numbers in roulette
            red_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
            result_color = "Red" if result_number in red_numbers else "Black" if result_number != 0 else "Green"
            result_parity = "Even" if result_number % 2 == 0 and result_number != 0 else "Odd" if result_number != 0 else "Zero"
            
            won = False
            multiplier = 0
            
            if "Number" in bet_type:
                if bet_choice == result_number:
                    won = True
                    multiplier = 35
            elif "Red/Black" in bet_type:
                if bet_choice == result_color:
                    won = True
                    multiplier = 2
            else:
                if bet_choice == result_parity:
                    won = True
                    multiplier = 2
            
            player.reduce_hunger(5)
            
            if won:
                winnings = bet_amount * multiplier
                player.add_money(winnings)
                player.casino_wins += 1
                player.add_xp(20)
                st.session_state.roulette_result = f"✅ Number: {result_number} ({result_color}) - YOU WIN ${winnings}!"
                show_success(st.session_state.roulette_result)
            else:
                player.remove_money(bet_amount)
                player.casino_losses += 1
                st.session_state.roulette_result = f"❌ Number: {result_number} ({result_color}) - You lost ${bet_amount}"
                show_error(st.session_state.roulette_result)
            
            check_death_conditions()
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Casino", use_container_width=True):
            navigate_to("casino")
    
    if st.session_state.roulette_result:
        st.markdown("---")
        st.markdown("### Last Result")
        st.markdown(f"**{st.session_state.roulette_result}**")
