"""Horse racing casino game."""
import streamlit as st
import random
import time
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header, show_success, show_error, render_money_bar

def render_horse_racing():
    """Render the horse racing game."""
    render_section_header("Horse Racing", "🏇")
    
    player = get_player()
    
    # Always show money bar
    render_money_bar()
    
    horses = ["🐴 Thunder", "🐎 Lightning", "🦄 Sparkle", "🏇 Flash", "🐴 Storm"]
    
    # Check if player has enough money
    if player.money < 10:
        st.warning("💸 You need at least $10 to play Horse Racing! Try Street Jobs to earn some money.")
        if st.button("🏠 Back to Casino", use_container_width=True):
            navigate_to("casino")
        return
    
    if 'race_result' not in st.session_state:
        st.session_state.race_result = None
    
    st.markdown("### Place Your Bet")
    
    bet_amount = st.number_input(
        "Enter bet amount:",
        min_value=10,
        max_value=player.money,
        value=min(50, player.money),
        step=10,
        key="horse_bet_input"
    )
    
    chosen_horse = st.selectbox("Pick a horse:", horses, key="horse_choice")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏁 Start Race", use_container_width=True):
            # Deduct bet upfront
            player.remove_money(bet_amount)
            
            # Simulate race
            st.markdown("### 🏁 Race in Progress...")
            
            # Random speeds for each horse
            speeds = {horse: random.randint(50, 100) for horse in horses}
            
            # Display progress
            progress_placeholder = st.empty()
            
            for i in range(10):
                progress_text = "### Race Progress\n"
                for horse in horses:
                    progress = int((speeds[horse] / 100) * (i + 1) * 10)
                    progress_text += f"{horse}: {'█' * progress}{'░' * (10 - progress)} {progress * 10}%\n\n"
                
                progress_placeholder.markdown(progress_text)
                time.sleep(0.2)
            
            # Determine winner
            winner = max(speeds, key=speeds.get)
            
            player.reduce_hunger(5)
            mark_significant_action()  # Mark for mafia event check
            
            if winner == chosen_horse:
                # Return bet + bet profit (1:1)
                winnings = bet_amount * 2
                player.add_money(winnings)
                player.casino_wins += 1
                player.add_xp(20)
                st.session_state.race_result = f"✅ {winner} WINS! You won ${bet_amount} profit!"
                show_success(st.session_state.race_result)
            else:
                player.casino_losses += 1
                st.session_state.race_result = f"❌ {winner} wins. You lost ${bet_amount}."
                show_error(st.session_state.race_result)
            
            check_death_conditions()
            time.sleep(1)
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Casino", use_container_width=True):
            st.session_state.race_result = None
            navigate_to("casino")
    
    if st.session_state.race_result:
        st.markdown("---")
        st.markdown("### Race Result")
        st.markdown(f"**{st.session_state.race_result}**")
