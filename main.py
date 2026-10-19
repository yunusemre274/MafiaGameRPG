"""Main application file - Entry point for the game."""
import streamlit as st
from game_state import initialize_game_state, navigate_to, get_player, check_death_conditions, activate_mafia_if_needed
from ui_components import render_stat_panel, render_game_title, menu_button, render_hunger_warning, render_hp_warning
from mafia import render_mafia_popup, should_trigger_mafia_event, trigger_mafia_event
from save_load import save_game, load_game
from inventory import get_inventory_summary, use_item

# Import all page renderers
from market import render_market
from hospital import render_hospital
from secure import render_secure
from gang import render_gang
from casino.blackjack import render_blackjack
from casino.roulette import render_roulette
from casino.dice import render_dice
from casino.coin_flip import render_coin_flip
from social import render_social, update_social
from casino.horse_racing import render_horse_racing
from mini_games import (render_mini_games, render_card_memory, render_math_challenge,
                        render_pattern_memory, render_code_breaker, render_number_guesser)

# Configure Streamlit page
st.set_page_config(
    page_title="Casino Mafia RPG",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize game state
initialize_game_state()

def render_main_menu():
    """Render the main menu."""
    render_game_title()
    
    # Show warnings
    render_hunger_warning()
    render_hp_warning()
    
    # Main menu options
    st.markdown("### 🎮 Main Menu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if menu_button("Casino", "🎰", key="menu_casino"):
            navigate_to("casino")
        
        if menu_button("Market", "🏪", key="menu_market"):
            navigate_to("market")
        
        if menu_button("Secure Building", "🛡️", key="menu_secure"):
            navigate_to("secure")
        
        if menu_button("Gang Building", "👥", key="menu_gang"):
            navigate_to("gang")
    
    with col2:
        count = len(st.session_state.social_requests)
        if menu_button(f"Sosyal ({count})", "📱", key="menu_social"):
            navigate_to("social")

        if menu_button("Hospital", "🏥", key="menu_hospital"):
            navigate_to("hospital")
        
        if menu_button("Street Jobs", "💼", key="menu_minigames"):
            navigate_to("mini_games")
        
        if menu_button("Inventory", "🎒", key="menu_inventory"):
            navigate_to("inventory")
        
        if menu_button("Character Stats", "📊", key="menu_stats"):
            navigate_to("stats")
        
        st.markdown("---")
        
        col_save, col_load = st.columns(2)
        with col_save:
            if st.button("💾 Save", use_container_width=True):
                success, message = save_game()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        
        with col_load:
            if st.button("📂 Load", use_container_width=True):
                success, message = load_game()
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

def render_casino_menu():
    """Render casino submenu."""
    from ui_components import render_section_header
    
    render_section_header("Casino", "🎰")
    
    st.markdown("### Choose Your Game")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if menu_button("Blackjack", "🃏", key="casino_blackjack"):
            navigate_to("blackjack")
        
        if menu_button("Roulette", "🎡", key="casino_roulette"):
            navigate_to("roulette")
    
    with col2:
        if menu_button("Dice (Zar)", "🎲", key="casino_dice"):
            navigate_to("dice")
        
        if menu_button("Horse Racing", "🏇", key="casino_horse"):
            navigate_to("horse_racing")
    
    if menu_button("Coin Flip · Yazı Tura", "🪙", key="casino_coin_flip"):
        navigate_to("coin_flip")

    st.markdown("---")
    
    if menu_button("🏠 Back to Main Menu", key="casino_back"):
        navigate_to("main_menu")

def render_inventory_page():
    """Render inventory page."""
    from ui_components import render_section_header, show_success, show_error
    
    render_section_header("Inventory", "🎒")
    
    inventory = get_inventory_summary()
    
    if not inventory:
        st.info("Your inventory is empty. Visit the market to buy items!")
    else:
        st.markdown("### Your Items")
        
        for item_name, item_data in inventory.items():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            
            with col1:
                emoji = {"food": "🍔"}.get(item_data["type"], "📦")
                st.markdown(f"**{emoji} {item_name}**")
            
            with col2:
                st.markdown(f"Qty: **{item_data['quantity']}**")
            
            with col3:
                if item_data["type"] == "food":
                    st.markdown(f"+{item_data['effect']} 🍔")
            
            with col4:
                if st.button("Use", key=f"use_{item_name}"):
                    success, message = use_item(item_name)
                    if success:
                        show_success(message)
                        st.rerun()
                    else:
                        show_error(message)
    
    st.markdown("---")
    
    if menu_button("🏠 Back to Main Menu", key="inventory_back"):
        navigate_to("main_menu")

def render_stats_page():
    """Render character stats page."""
    from ui_components import render_section_header
    
    render_section_header("Character Stats", "📊")
    
    player = get_player()
    
    # Create columns for a cleaner layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("💰 Money", f"${player.money:,}")
        st.metric("❤️ HP", f"{player.hp}/{player.max_hp}")
        st.metric("🍔 Hunger", f"{player.hunger}/{player.max_hunger}")
        st.metric("⭐ Level", player.level)
        st.metric("✨ XP", f"{player.xp}/{player.level * 100}")
    
    with col2:
        st.metric("🛡️ Bodyguards", player.bodyguards)
        st.metric("👥 Gang Members", player.gang_members)
        st.metric("🎮 Total Actions", player.total_actions)
        st.metric("✅ Casino Wins", player.casino_wins)
        st.metric("❌ Casino Losses", player.casino_losses)
    
    st.markdown("---")
    
    if menu_button("🏠 Back to Main Menu", key="stats_back"):
        navigate_to("main_menu")

def render_game_over():
    """Render game over screen."""
    st.markdown("""
        <div style='background: linear-gradient(135deg, #c31432 0%, #240b36 100%);
                    padding: 50px; border-radius: 15px; text-align: center; color: white;'>
            <div style='font-size: 72px; margin-bottom: 20px;'>☠️</div>
            <div style='font-size: 48px; font-weight: bold; margin-bottom: 20px;'>GAME OVER</div>
            <div style='font-size: 24px; margin-bottom: 30px;'>
                {reason}
            </div>
        </div>
    """.format(reason=st.session_state.game_over_reason), unsafe_allow_html=True)
    
    player = get_player()
    
    st.markdown(f"""
        <div style='background: #f8f9fa; padding: 30px; border-radius: 10px; 
                    margin-top: 30px; text-align: center;'>
            <h3>Final Statistics</h3>
            <div style='font-size: 20px; margin: 10px 0;'>
                💰 Final Money: ${player.money:,}
            </div>
            <div style='font-size: 20px; margin: 10px 0;'>
                ⭐ Level Reached: {player.level}
            </div>
            <div style='font-size: 20px; margin: 10px 0;'>
                🎮 Total Actions: {player.total_actions}
            </div>
            <div style='font-size: 20px; margin: 10px 0;'>
                ✅ Casino Wins: {player.casino_wins} | ❌ Losses: {player.casino_losses}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Start New Game", use_container_width=True):
        # Reset all game state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    """Main application loop."""
    check_death_conditions()
    # Check for game over
    if st.session_state.game_over:
        render_game_over()
        return
    
    # Check mafia activation
    if activate_mafia_if_needed():
        st.toast("⚠️ The mafia is now watching you!", icon="🔫")
    
    update_social()

    # Check ordinary events before queued social raids so neither replaces the other.
    if not st.session_state.mafia_event_pending and should_trigger_mafia_event():
        st.session_state.normal_mafia_queued = True
    if not st.session_state.mafia_event_pending:
        if st.session_state.normal_mafia_queued:
            st.session_state.normal_mafia_queued = False
            trigger_mafia_event()
        elif st.session_state.social_raids:
            raid = st.session_state.social_raids.pop(0)
            trigger_mafia_event(group_id=raid["group_id"], source="social", contact_id=raid["contact_id"])

    render_stat_panel()
    # Render mafia popup if pending
    if render_mafia_popup():
        return  # Don't render other content while mafia popup is active
    
    # Route to appropriate page
    page = st.session_state.current_page
    
    if page == "main_menu":
        render_main_menu()
    elif page == "casino":
        render_casino_menu()
    elif page == "blackjack":
        render_blackjack()
    elif page == "roulette":
        render_roulette()
    elif page == "social":
        render_social()
    elif page == "coin_flip":
        render_coin_flip()
    elif page == "dice":
        render_dice()
    elif page == "horse_racing":
        render_horse_racing()
    elif page == "market":
        render_market()
    elif page == "hospital":
        render_hospital()
    elif page == "secure":
        render_secure()
    elif page == "gang":
        render_gang()
    elif page == "inventory":
        render_inventory_page()
    elif page == "stats":
        render_stats_page()
    elif page == "mini_games":
        if 'current_minigame' in st.session_state and st.session_state.current_minigame:
            if st.session_state.current_minigame == "card_memory":
                render_card_memory()
            elif st.session_state.current_minigame == "math_challenge":
                render_math_challenge()
            elif st.session_state.current_minigame == "pattern_memory":
                render_pattern_memory()
            elif st.session_state.current_minigame == "code_breaker":
                render_code_breaker()
            elif st.session_state.current_minigame == "number_guesser":
                render_number_guesser()
        else:
            render_mini_games()
    else:
        render_main_menu()

if __name__ == "__main__":
    main()
