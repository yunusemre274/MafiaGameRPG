"""Dice (Zar) casino game."""
import streamlit as st
import random
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header, show_success, show_error, show_info, render_money_bar

def render_dice():
    """Render the dice game."""
    render_section_header("Dice Game (Zar)", "🎲")
    
    player = get_player()
    
    # Always show money bar
    render_money_bar()
    
    # Check if player has enough money
    if player.money < 10:
        st.warning("💸 You need at least $10 to play Dice! Try Street Jobs to earn some money.")
        if st.button("🏠 Back to Casino", use_container_width=True):
            navigate_to("casino")
        return
    
    st.markdown("### How to Play")
    st.info("Roll 2 dice and bet on the total sum (2-12). Exact match: 10x, Close (±1): 3x")
    
    bet_amount = st.number_input(
        "Enter bet amount:",
        min_value=10,
        max_value=player.money,
        value=min(50, player.money),
        step=10,
        key="dice_bet_input"
    )
    
    bet_number = st.slider("Predict the sum:", 2, 12, 7, key="dice_prediction")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎲 Roll Dice", use_container_width=True):
            # Deduct bet upfront
            player.remove_money(bet_amount)
            
            dice1 = random.randint(1, 6)
            dice2 = random.randint(1, 6)
            total = dice1 + dice2
            
            st.session_state.dice_result = (dice1, dice2, total)
            
            player.reduce_hunger(5)
            mark_significant_action()  # Mark for mafia event check
            
            if total == bet_number:
                # Exact match - return bet + 1x profit (2x total)
                winnings = bet_amount * 2
                player.add_money(winnings)
                player.casino_wins += 1
                player.add_xp(25)
                show_success(f"🎉 EXACT MATCH! Rolled {dice1} + {dice2} = {total}. Won ${bet_amount} profit!")
            elif abs(total - bet_number) == 1:
                # Close match - return bet + 0.5x profit
                winnings = int(bet_amount * 1.5)
                player.add_money(winnings)
                player.casino_wins += 1
                player.add_xp(10)
                show_info(f"Close! Rolled {dice1} + {dice2} = {total}. Won ${winnings - bet_amount} profit!")
            else:
                player.casino_losses += 1
                show_error(f"Lost! Rolled {dice1} + {dice2} = {total}. Lost ${bet_amount}.")
            
            check_death_conditions()
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Casino", use_container_width=True):
            navigate_to("casino")
    
    if hasattr(st.session_state, 'dice_result'):
        dice1, dice2, total = st.session_state.dice_result
        st.markdown("---")
        st.markdown("### Last Roll")
        st.markdown(f"""
            <div style='text-align: center; font-size: 60px;'>
                🎲 {dice1}  +  🎲 {dice2}  =  {total}
            </div>
        """, unsafe_allow_html=True)
