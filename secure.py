"""Secure building for hiring bodyguards."""
import streamlit as st
from game_state import get_player, navigate_to
from ui_components import render_section_header, show_success, show_error, show_info

UNLOCK_AMOUNT = 25000
BODYGUARD_COST = 5000

def render_secure():
    """Render the secure building interface."""
    render_section_header("Secure Building", "🛡️")
    
    player = get_player()
    
    if player.money < UNLOCK_AMOUNT and player.bodyguards == 0:
        st.markdown("""
            <div style='background: #ff6b6b; padding: 30px; border-radius: 10px; 
                        text-align: center; color: white; margin: 20px 0;'>
                <div style='font-size: 40px; margin-bottom: 10px;'>🔒 LOCKED</div>
                <div style='font-size: 24px;'>
                    This building is locked!
                </div>
                <div style='font-size: 20px; margin-top: 10px;'>
                    Requires: <span style='font-weight: bold;'>${:,}</span>
                </div>
                <div style='font-size: 18px; margin-top: 10px; color: #ffeeee;'>
                    You currently have: ${:,}
                </div>
            </div>
        """.format(UNLOCK_AMOUNT, player.money), unsafe_allow_html=True)
        
        if st.button("🏠 Back to Main Menu", use_container_width=True):
            navigate_to("main_menu")
        return
    
    st.markdown("### 🛡️ Bodyguard Services")
    
    st.info("""
    **Bodyguards:**
    - Never die
    - Do NOT fight mafia
    - Reduce incoming damage by 5 HP per bodyguard
    - Passive permanent protection
    """)
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px; border-radius: 10px; color: white; margin: 20px 0;'>
            <div style='text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>Current Bodyguards: {player.bodyguards}</div>
                <div style='font-size: 18px; margin-top: 10px;'>
                    Damage Reduction: -{player.bodyguards * 5} HP per attack
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 10px; 
                    text-align: center; margin: 20px 0;'>
            <div style='font-size: 20px; font-weight: bold;'>💼 Hire Bodyguard</div>
            <div style='font-size: 24px; color: #28a745; margin-top: 10px;'>
                Cost: ${BODYGUARD_COST:,}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛡️ Hire Bodyguard", use_container_width=True):
            if player.can_afford(BODYGUARD_COST):
                player.remove_money(BODYGUARD_COST)
                player.bodyguards += 1
                player.add_xp(10)
                show_success(f"Hired a bodyguard! You now have {player.bodyguards} bodyguard(s).")
                st.rerun()
            else:
                show_error(f"Not enough money! You need ${BODYGUARD_COST:,}.")
    
    with col2:
        if st.button("🏠 Back to Main Menu", use_container_width=True):
            navigate_to("main_menu")
