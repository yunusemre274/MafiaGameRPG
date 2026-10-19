"""Fair 50/50 coin flip."""
import random
import streamlit as st
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header


def flip_coin():
    return random.choice(['Yazı', 'Tura'])


def render_coin_flip():
    render_section_header('Yazı Tura', '🪙')
    player = get_player()
    result = st.session_state.get('coin_result')
    face = result['face'] if result else '?'
    st.markdown(f"<style>@keyframes coin-turn{{from{{transform:rotateY(720deg)}}to{{transform:rotateY(0)}}}}"
                ".rpg-coin{animation:coin-turn 1.2s ease-out;background:radial-gradient(circle at 30% 25%,#fff1b6,#d4a43b 60%,#866020);"
                "border:8px double #f8d67e;border-radius:50%;width:180px;height:180px;display:grid;place-items:center;"
                "margin:24px auto;color:#573b12;font-size:34px;font-weight:800;box-shadow:0 15px 30px #0004}</style>"
                f"<div class='rpg-coin'>{face}</div>", unsafe_allow_html=True)
    st.caption('Yazı %50 · Tura %50 · Kazançta toplam ödeme 2× bahis.')
    if result:
        (st.success if result['won'] else st.error)(f"{result['face']} geldi! Net ${result['net']:+,}")
    if player.money >= 10:
        bet = st.number_input('Bahis ($)', min_value=10, max_value=player.money,
                              value=min(50, player.money), step=10, key='coin_bet_input')
        choice = st.radio('Seçimin', ['Yazı', 'Tura'], horizontal=True, key='coin_choice')
        if st.button('🪙 Parayı çevir', type='primary', use_container_width=True):
            face = flip_coin()
            won = face == choice
            player.remove_money(bet)
            if won:
                player.add_money(bet * 2)
                player.casino_wins += 1
                player.add_xp(15)
            else:
                player.casino_losses += 1
            player.reduce_hunger(5)
            mark_significant_action()
            st.session_state.coin_result = dict(face=face, won=won, net=bet if won else -bet)
            check_death_conditions()
            st.rerun()
    else:
        st.warning('Oynamak için en az $10 gerekiyor.')
    if st.button('🏠 Back to Casino', key='coin_back', use_container_width=True):
        navigate_to('casino')
