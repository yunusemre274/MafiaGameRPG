"""Reusable UI components for the game."""
import streamlit as st
from game_state import get_player

def render_stat_panel():
    """Render the persistent stats panel at the top."""
    player = get_player()
    
    st.markdown("""
        <style>
        .stat-panel {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stat-row {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            font-size: 18px;
            font-weight: bold;
        }
        .stat-item {
            flex: 1;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="stat-panel">
            <div class="stat-row">
                <div class="stat-item">💰 Money: ${player.money:,}</div>
                <div class="stat-item">❤️ HP: {player.hp}/{player.max_hp}</div>
            </div>
            <div class="stat-row">
                <div class="stat-item">🍔 Hunger: {player.hunger}/{player.max_hunger}</div>
                <div class="stat-item">⭐ Level: {player.level} (XP: {player.xp}/{player.level * 100})</div>
            </div>
            <div class="stat-row">
                <div class="stat-item">🛡️ Bodyguards: {player.bodyguards}</div>
                <div class="stat-item">👥 Gang: {player.gang_members}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_game_title():
    """Render the game title."""
    st.markdown("""
        <style>
        .game-title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .game-subtitle {
            text-align: center;
            font-size: 18px;
            color: #666;
            margin-bottom: 30px;
        }
        </style>
        <div class="game-title">🎰 Casino Mafia RPG 🔫</div>
        <div class="game-subtitle">A 1D Menu-Based Decision Game</div>
    """, unsafe_allow_html=True)

def menu_button(label, emoji="", key=None):
    """Create a styled menu button."""
    button_label = f"{emoji} {label}" if emoji else label
    return st.button(button_label, key=key, use_container_width=True)

def show_warning(message):
    """Show a warning message."""
    st.warning(f"⚠️ {message}")

def show_success(message):
    """Show a success message."""
    st.success(f"✅ {message}")

def show_error(message):
    """Show an error message."""
    st.error(f"❌ {message}")

def show_info(message):
    """Show an info message."""
    st.info(f"ℹ️ {message}")

def render_section_header(title, emoji=""):
    """Render a section header."""
    header_text = f"{emoji} {title}" if emoji else title
    st.markdown(f"### {header_text}")
    st.markdown("---")

def render_hunger_warning():
    """Show warning if hunger is low."""
    player = get_player()
    if player.hunger == 0:
        show_error("You are starving! Every action will reduce your HP!")
    elif player.hunger < 20:
        show_warning("Your hunger is very low! Buy food soon!")

def render_hp_warning():
    """Show warning if HP is low."""
    player = get_player()
    if player.hp < 30:
        show_error(f"Your HP is critical! ({player.hp}/{player.max_hp}) Visit the hospital!")
    elif player.hp < 50:
        show_warning(f"Your HP is low. ({player.hp}/{player.max_hp})")
