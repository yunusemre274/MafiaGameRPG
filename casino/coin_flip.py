"""Fair 50/50 coin flip with a three-second, two-sided gold coin."""
import random
from pathlib import Path
from uuid import uuid4
import streamlit as st
import streamlit.components.v1 as components
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header

_coin = components.declare_component('mafia_gold_coin', path=str(Path(__file__).parent / 'coin_frontend'))


def flip_coin():
    return random.choice(['Yazı', 'Tura'])


def finish_flip(round_id):
    """Charge and settle only the matching pending round, once animation ends."""
    pending = st.session_state.get('coin_pending')
    if not pending or pending['id'] != round_id:
        return False
    player = get_player()
    bet, won = pending['bet'], pending['won']
    player.remove_money(bet)
    if won:
        player.add_money(bet * 2)
        player.casino_wins += 1
        player.add_xp(15)
    else:
        player.casino_losses += 1
    player.reduce_hunger(5)
    mark_significant_action()
    st.session_state.coin_result = dict(face=pending['face'], won=won, net=bet if won else -bet)
    st.session_state.coin_pending = None
    check_death_conditions()
    return True


def render_coin_flip():
    render_section_header('Yazı Tura', '🪙')
    player = get_player()
    pending = st.session_state.get('coin_pending')
    result = st.session_state.get('coin_result')
    face = pending['face'] if pending else result['face'] if result else 'Yazı'
    event = _coin(face=face, spinning=bool(pending), round_id=pending['id'] if pending else None,
                  key='coin_animation', default=None)
    if pending and isinstance(event, dict) and event.get('finished') is True:
        if finish_flip(event.get('round_id')):
            st.rerun()
    st.caption('Yazı: 5 euro · Tura: tavşan logosu · İkisi de %50 · Kazançta toplam ödeme 2× bahis.')
    if result and not pending:
        (st.success if result['won'] else st.error)(f"{result['face']} geldi! Net ${result['net']:+,}")
    if player.money >= 10:
        bet = st.number_input('Bahis ($)', min_value=10, max_value=player.money,
                              value=min(50, player.money), step=10, key='coin_bet_input', disabled=bool(pending))
        choice = st.radio('Seçimin', ['Yazı', 'Tura'], horizontal=True, key='coin_choice',
                          format_func=lambda value: 'Yazı · 5 €' if value == 'Yazı' else 'Tura · Tavşan',
                          disabled=bool(pending))
        if st.button('🪙 Parayı çevir', type='primary', use_container_width=True, disabled=bool(pending)):
            face = flip_coin()
            st.session_state.coin_pending = dict(id=uuid4().hex, face=face, won=face == choice, bet=bet)
            st.rerun()
    else:
        st.warning('Oynamak için en az $10 gerekiyor.')
    if st.button('🏠 Back to Casino', key='coin_back', use_container_width=True, disabled=bool(pending)):
        navigate_to('casino')
