"""Hospital system for healing."""
import streamlit as st
from game_state import get_player, navigate_to, check_death_conditions
from ui_components import render_section_header, show_success, show_error, menu_button

HEAL_COST = 1500

def render_hospital():
    """Render the hospital interface."""
    render_section_header("Hospital", "🏥")
    
    player = get_player()
    
    st.markdown("### Medical Services")
    
    # Display current HP
    hp_percentage = (player.hp / player.max_hp) * 100
    color = "#28a745" if hp_percentage > 50 else "#ffc107" if hp_percentage > 25 else "#dc3545"
    
    st.markdown(f"""
        <div style='padding: 20px; border: 2px solid {color}; border-radius: 10px; margin: 20px 0;'>
            <div style='text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>Current HP</div>
                <div style='font-size: 48px; color: {color};'>{player.hp}/{player.max_hp}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 10px; margin: 20px 0;'>
            <div style='text-align: center;'>
                <div style='font-size: 20px; font-weight: bold;'>💉 Full Healing</div>
                <div style='font-size: 18px; color: #666; margin: 10px 0;'>
                    Restore HP to {player.max_hp}
                </div>
                <div style='font-size: 24px; color: #28a745; font-weight: bold;'>
                    Cost: ${HEAL_COST}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if player.hp >= player.max_hp:
            st.info("You are already at full health!")
        elif st.button("💊 Heal to Full HP", key="heal_button", use_container_width=True):
            if player.can_afford(HEAL_COST):
                player.remove_money(HEAL_COST)
                player.heal()
                player.reduce_hunger(5)
                player.add_xp(10)
                show_success(f"Healed to full HP! Paid ${HEAL_COST}.")
                check_death_conditions()
                st.rerun()
            else:
                show_error(f"Not enough money! You need ${HEAL_COST}.")
    
    st.markdown("---")
    
    if menu_button("🏠 Back to Main Menu", key="hospital_back"):
        navigate_to("main_menu")
