"""Mafia system with extortion and combat."""
import streamlit as st
import random
from game_state import get_player, check_death_conditions
from ui_components import show_success, show_error, show_warning, show_info

def should_trigger_mafia_event():
    """Check if mafia event should trigger."""
    if not st.session_state.mafia_active:
        return False
    
    # 15% chance after each significant action
    return random.random() < 0.15

def trigger_mafia_event():
    """Trigger a mafia extortion event."""
    player = get_player()
    
    # Calculate extortion amount (5-15% of current money)
    percentage = random.uniform(0.05, 0.15)
    extortion_amount = int(player.money * percentage)
    extortion_amount = max(500, extortion_amount)  # Minimum $500
    
    st.session_state.mafia_event_pending = True
    st.session_state.mafia_demand_amount = extortion_amount

def render_mafia_popup():
    """Render the mafia extortion popup."""
    if not st.session_state.mafia_event_pending:
        return False
    
    player = get_player()
    demand = st.session_state.mafia_demand_amount
    
    st.markdown("""
        <div style='background: linear-gradient(135deg, #c31432 0%, #240b36 100%); 
                    padding: 30px; border-radius: 15px; border: 3px solid #ff0000;
                    text-align: center; color: white; margin: 20px 0;'>
            <div style='font-size: 48px; margin-bottom: 10px;'>🔫 MAFIA EXTORTION 🔫</div>
            <div style='font-size: 24px; margin: 20px 0;'>
                The mafia demands <span style='color: #ffff00; font-weight: bold;'>${:,}</span> in extortion money!
            </div>
            <div style='font-size: 18px; color: #ffaaaa;'>
                What will you do?
            </div>
        </div>
    """.format(demand), unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💰 Pay Extortion", key="mafia_pay", use_container_width=True):
            if player.can_afford(demand):
                player.remove_money(demand)
                player.add_xp(5)
                show_success(f"Paid ${demand:,} to the mafia. They leave you alone... for now.")
                st.session_state.mafia_event_pending = False
                check_death_conditions()
                st.rerun()
            else:
                show_error("You don't have enough money to pay!")
    
    with col2:
        if st.button("⚔️ REJECT and Fight", key="mafia_reject", use_container_width=True):
            resolve_mafia_combat()
            st.session_state.mafia_event_pending = False
            st.rerun()
    
    return True

def resolve_mafia_combat():
    """Resolve combat with the mafia."""
    player = get_player()
    
    # Random number of mafia attackers
    mafia_count = random.randint(1, 3)
    
    show_warning(f"⚔️ {mafia_count} Mafia members attack!")
    
    if player.gang_members > 0:
        # Gang fights
        st.markdown("### 👥 Gang Battle!")
        
        for i in range(mafia_count):
            # Each mafia member is killed
            show_info(f"Your gang killed 1 mafia member!")
            
            # Calculate gang losses
            if player.level < 5:
                gang_loss = 1
            else:
                gang_loss = 2
            
            player.gang_members = max(0, player.gang_members - gang_loss)
            show_warning(f"Lost {gang_loss} gang member(s)")
        
        # If gang is depleted, mafia attacks player directly
        if player.gang_members <= 0:
            remaining_mafia = random.randint(0, 1)
            if remaining_mafia > 0:
                damage = remaining_mafia * 20
                actual_damage = player.take_damage(damage)
                show_error(f"Gang wiped out! Took {actual_damage} damage from remaining mafia!")
            else:
                show_success("Gang fought them off, but all members died!")
        else:
            show_success(f"Gang survived! {player.gang_members} members remaining.")
            player.add_xp(30)
    
    else:
        # No gang, direct attack
        st.markdown("### 💥 Direct Attack!")
        damage = random.randint(30, 50)
        actual_damage = player.take_damage(damage)
        show_error(f"Mafia attacked you directly! Took {actual_damage} damage!")
    
    check_death_conditions()
