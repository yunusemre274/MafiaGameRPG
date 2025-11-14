"""Gang building for recruiting gang members."""
import streamlit as st
from game_state import get_player, navigate_to
from ui_components import render_section_header, show_success, show_error, show_info

UNLOCK_AMOUNT = 50000
GANG_MEMBER_COST = 3000

def render_gang():
    """Render the gang building interface."""
    render_section_header("Gang Building", "👥")
    
    player = get_player()
    
    if player.money < UNLOCK_AMOUNT and player.gang_members == 0:
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
    
    st.markdown("### 👥 Gang Recruitment")
    
    st.info("""
    **Gang Members:**
    - Fight mafia in combat
    - Die during battles
    - Act as HP shield before you take damage
    - Loss rate depends on your level:
      - Level 1-4: Lose 1 member per mafia
      - Level 5+: Lose 2 members per mafia
    """)
    
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    padding: 20px; border-radius: 10px; color: white; margin: 20px 0;'>
            <div style='text-align: center;'>
                <div style='font-size: 24px; font-weight: bold;'>Current Gang Members: {player.gang_members}</div>
                <div style='font-size: 18px; margin-top: 10px;'>
                    Your Level: {player.level}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 10px; 
                    text-align: center; margin: 20px 0;'>
            <div style='font-size: 20px; font-weight: bold;'>💼 Recruit Gang Member</div>
            <div style='font-size: 24px; color: #28a745; margin-top: 10px;'>
                Cost: ${GANG_MEMBER_COST:,}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👊 Recruit Member", use_container_width=True):
            if player.can_afford(GANG_MEMBER_COST):
                player.remove_money(GANG_MEMBER_COST)
                player.gang_members += 1
                player.add_xp(15)
                show_success(f"Recruited a gang member! You now have {player.gang_members} member(s).")
                st.rerun()
            else:
                show_error(f"Not enough money! You need ${GANG_MEMBER_COST:,}.")
    
    with col2:
        if st.button("🏠 Back to Main Menu", use_container_width=True):
            navigate_to("main_menu")
