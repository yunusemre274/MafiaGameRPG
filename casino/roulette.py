"""European roulette with a clickable felt table and server-authoritative bets."""
import random
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header

RED_NUMBERS = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
WHEEL_ORDER = [0,32,15,19,4,21,2,25,17,34,6,27,13,36,11,30,8,23,10,5,24,16,33,1,20,14,31,9,22,18,29,7,28,12,35,3,26]
_table = components.declare_component('mafia_roulette_table', path=str(Path(__file__).parent / 'roulette_frontend'))


def bet_catalog():
    """Canonical coverage and total returns (stake included). Never trust client odds."""
    catalog = {}
    def add(key, label, numbers):
        catalog[key] = {'id': key, 'label': label, 'numbers': sorted(numbers), 'multiplier': 36 // len(numbers)}
    for number in range(37):
        add(f'n{number}', str(number), [number])
    for number in range(1, 37):
        if number % 3 != 0:
            add(f's{number}_{number+1}', f'Split {number}/{number+1}', [number,number+1])
        if number <= 33:
            add(f's{number}_{number+3}', f'Split {number}/{number+3}', [number,number+3])
        if number <= 32 and number % 3 != 0:
            add(f'c{number}', f'Corner {number}/{number+1}/{number+3}/{number+4}', [number,number+1,number+3,number+4])
    for n in [1,2,3]:
        add(f's0_{n}', f'Split 0/{n}', [0,n])
    add('trio01', 'Trio 0/1/2', [0,1,2])
    add('trio02', 'Trio 0/2/3', [0,2,3])
    add('first4', 'First four 0/1/2/3', [0,1,2,3])
    for start in range(1, 37, 3):
        add(f'street{start}', f'Street {start}–{start+2}', range(start,start+3))
        if start < 34:
            add(f'line{start}', f'Six line {start}–{start+5}', range(start,start+6))
    for i in range(3):
        add(f'dozen{i}', f'{i*12+1}–{i*12+12}', range(i*12+1,i*12+13))
        add(f'column{i}', f'Column {i+1}', range(i+1,37,3))
    add('red', 'Kırmızı', RED_NUMBERS)
    add('black', 'Siyah', set(range(1,37))-RED_NUMBERS)
    add('even', 'Çift', range(2,37,2))
    add('odd', 'Tek', range(1,37,2))
    add('low', '1–18', range(1,19))
    add('high', '19–36', range(19,37))
    return catalog


CATALOG = bet_catalog()


def validate_bets(raw_bets, balance):
    if not isinstance(raw_bets, list) or not raw_bets or len(raw_bets) > len(CATALOG):
        raise ValueError('Masaya en az bir bahis koy.')
    bets, seen = [], set()
    for entry in raw_bets:
        if not isinstance(entry, dict):
            raise ValueError('Geçersiz bahis.')
        key, amount = entry.get('id'), entry.get('amount')
        if not isinstance(key, str) or key not in CATALOG or key in seen or type(amount) is not int or amount < 10 or amount % 10:
            raise ValueError('Geçersiz fiş veya bahis.')
        seen.add(key)
        bets.append({'id': key, 'amount': amount})
    if sum(b['amount'] for b in bets) > balance:
        raise ValueError('Bakiyen bu bahisler için yetersiz.')
    return bets


def spin_number():
    # Each pocket has the same probability, independent of wagers or player stats.
    return random.randint(0, 36)


def total_return(bets, number):
    return sum(bet['amount'] * CATALOG[bet['id']]['multiplier']
               for bet in bets if number in CATALOG[bet['id']]['numbers'])


def play_spin(raw_bets):
    player = get_player()
    bets = validate_bets(raw_bets, player.money)
    stake = sum(b['amount'] for b in bets)
    number = spin_number()
    payout = total_return(bets, number)
    player.remove_money(stake)
    if payout:
        player.add_money(payout)
    net = payout-stake
    if net > 0:
        player.casino_wins += 1
        player.add_xp(20)
    elif net < 0:
        player.casino_losses += 1
    player.reduce_hunger(5)
    mark_significant_action()
    check_death_conditions()
    return dict(number=number, stake=stake, payout=payout, net=net)


def render_roulette():
    render_section_header('Rulet · Avrupa Masası', '🎡')
    st.caption('Tek sıfırlı masa · 0–36 arasındaki her sayı eşit olasılıklıdır. '
               'Birden fazla alana fiş koyabilirsin. Sıfır geldiğinde dış bahisler kaybeder.')
    player = get_player()
    state = st.session_state.setdefault('roulette_state', {})
    event = _table(balance=player.money, catalog=CATALOG, wheel=WHEEL_ORDER,
                   last_result=state.get('last_result'), history=state.get('history', []),
                   revision=state.get('revision', 0), key='roulette_table', default=None)
    if isinstance(event, dict) and isinstance(event.get('event_id'), str) and event['event_id'] != state.get('handled_event'):
        state['handled_event'] = event['event_id']
        try:
            result = play_spin(event.get('bets'))
            state['revision'] = state.get('revision', 0)+1
            state['last_result'] = result
            state['history'] = ([result['number']] + state.get('history', []))[:12]
            state.pop('error', None)
        except ValueError as error:
            state['error'] = str(error)
        st.rerun()
    if state.get('error'):
        st.warning(state['error'])
    if st.button('🏠 Back to Casino', key='roulette_back', use_container_width=True):
        navigate_to('casino')
