"""Reusable UI components for the game."""
import streamlit as st
from game_state import get_player

def render_stat_panel():
    """Live meters shared by every page, including all casino games."""
    player = get_player()
    def meter(label, value, maximum, color, detail):
        percent = max(0, min(100, value / maximum * 100))
        return (f'<div class="rpg-meter"><div class="rpg-meter-label">'
                f'<span>{label}</span><strong>{detail}</strong></div>'
                f'<div class="rpg-track" role="progressbar" aria-label="{label}" '
                f'aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="{maximum}">'
                f'<div style="width:{percent}%;background:{color}"></div></div></div>')
    bars = ''.join([
        meter('❤️ Can', player.hp, player.max_hp, '#f87171', f'{player.hp}/{player.max_hp}'),
        meter('🍔 Tokluk', player.hunger, player.max_hunger, '#fbbf24', f'{player.hunger}/{player.max_hunger}'),
        meter(f'⭐ Seviye {player.level}', player.xp, player.level * 100, '#a78bfa', f'{player.xp}/{player.level * 100} XP'),
        meter('🛡️ Bodyguard', min(player.bodyguards, 10), 10, '#38bdf8', f'{player.bodyguards} · −{player.bodyguards * 5} hasar'),
        meter('🧠 Stres', player.stress, 100, '#fb7185' if player.stress >= 60 else '#2dd4bf', f'{player.stress:.0f}/100'),
    ])
    st.markdown("""<style>
    .rpg-panel{background:linear-gradient(120deg,#111827,#172a36);border:1px solid #334155;
    border-radius:16px;padding:20px 24px;margin:0 0 24px;color:#f8fafc}
    .rpg-head{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}
    .rpg-cash{color:#f5d58b;font-size:26px;font-weight:800}
    .rpg-bars{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:20px}
    .rpg-meter-label{display:flex;justify-content:space-between;gap:8px;font-size:12px;margin-bottom:9px}
    .rpg-track{background:#ffffff18;border-radius:8px;height:9px;overflow:hidden}
    .rpg-track>div{height:100%;border-radius:8px;transition:width .35s}
    .rpg-note{font-size:11px;color:#94a3b8;margin-top:12px}
    </style>""" + f'<div class="rpg-panel"><div class="rpg-head"><span class="rpg-cash">${player.money:,}</span>'
    f'<span>👥 {player.gang_members} Gang · 🎮 {player.total_actions} eylem</span></div>'
    f'<div class="rpg-bars">{bars}</div><div class="rpg-note">Stres yalnızca görseldir. '
    'Bodyguard barı 10 korumada dolar; ek korumalar da hasarı azaltır.</div></div>', unsafe_allow_html=True)


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

def render_money_bar():
    """Render a compact money display bar for use in casino games."""
    player = get_player()
    st.markdown(f"""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                    padding: 10px 20px; border-radius: 8px; margin-bottom: 15px;
                    color: white; font-size: 20px; font-weight: bold; text-align: center;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>
            💰 Your Money: ${player.money:,}
        </div>
    """, unsafe_allow_html=True)

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
