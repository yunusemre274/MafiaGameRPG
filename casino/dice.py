"""Two dice: predict whether the total is lower or higher than a changing target."""
import random
import streamlit as st
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header


def next_target(previous=None):
    # Two six-sided dice total 2..12. Both choices remain possible at 3..11.
    return random.choice([n for n in range(3, 12) if n != previous])


def dice_outcome(total, target, choice):
    if total == target:
        return 'push'
    return 'win' if (total < target) == (choice == 'Düşük') else 'loss'


def render_dice():
    render_section_header('Zar · Düşük / Yüksek', '🎲')
    player = get_player()
    if 'dice_target' not in st.session_state:
        st.session_state.dice_target = next_target()
    result = st.session_state.get('dice_round_result')
    if result:
        icon = {'win': '✅', 'loss': '❌', 'push': '↔️'}[result['outcome']]
        st.info(f"{icon} Son raund: {result['dice'][0]} + {result['dice'][1]} = {sum(result['dice'])} · "
                f"Hedef {result['target']} · {result['choice']} · Net ${result['net']:+,}")
    st.markdown(f"<div style='background:#112f2b;border:1px solid #b79a53;border-radius:20px;"
                f"padding:32px;text-align:center;color:#f6e8bc'><div>BU RAUNDUN HEDEFİ</div>"
                f"<div style='font-size:80px;font-weight:800'>{st.session_state.dice_target}</div>"
                "<div>🎲 + 🎲 · Toplam daha düşük mü, daha yüksek mi?</div></div>", unsafe_allow_html=True)
    st.caption('İki adet altı yüzlü zar atılır. Kazanınca toplam ödeme 2×; hedefle eşitlikte bahis iade. Hedef her raund değişir (3–11).')
    if player.money >= 10:
        bet = st.number_input('Bahis ($)', min_value=10, max_value=player.money,
                              value=min(50, player.money), step=10, key='dice_bet_input')
        choice = st.radio('Tahminin', ['Düşük', 'Yüksek'], horizontal=True, key='dice_choice')
        if st.button('🎲 Zarları at', type='primary', use_container_width=True):
            target = st.session_state.dice_target
            dice = [random.randint(1, 6), random.randint(1, 6)]
            outcome = dice_outcome(sum(dice), target, choice)
            player.remove_money(bet)
            payout = bet * 2 if outcome == 'win' else bet if outcome == 'push' else 0
            if payout:
                player.add_money(payout)
            if outcome == 'win':
                player.casino_wins += 1
                player.add_xp(15)
            elif outcome == 'loss':
                player.casino_losses += 1
            player.reduce_hunger(5)
            mark_significant_action()
            st.session_state.dice_round_result = dict(dice=dice, target=target, choice=choice, outcome=outcome, net=payout-bet)
            st.session_state.dice_target = next_target(target)
            check_death_conditions()
            st.rerun()
    else:
        st.warning('Oynamak için en az $10 gerekiyor.')
    if st.button('🏠 Back to Casino', key='dice_back', use_container_width=True):
        navigate_to('casino')
