"""Blackjack with independently wagered split hands and one-time settlement."""
import random
from html import escape
import streamlit as st
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header


class Card:
    def __init__(self, suit, rank):
        self.suit, self.rank = suit, rank

    def value(self):
        return 11 if self.rank == 'A' else 10 if self.rank in ['J', 'Q', 'K'] else int(self.rank)

    def __str__(self):
        return f"{self.rank}{ {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}[self.suit]}"


def create_deck():
    deck = [Card(suit, rank) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            for rank in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']]
    random.shuffle(deck)
    return deck


def calculate_hand_value(hand):
    value = sum(card.value() for card in hand)
    for _ in range(sum(card.rank == 'A' for card in hand)):
        if value > 21:
            value -= 10
    return value


def start_round(player, bet, deck=None):
    if not isinstance(bet, int) or bet < 10 or not player.can_afford(bet):
        raise ValueError('Geçersiz bahis.')
    deck = create_deck() if deck is None else deck
    player.remove_money(bet)
    return {'active': True, 'settled': False, 'deck': deck,
            'hands': [{'cards': [deck.pop(), deck.pop()], 'bet': bet, 'done': False}],
            'dealer': [deck.pop(), deck.pop()], 'index': 0, 'split': False,
            'double_rule': False, 'results': []}


def can_split(game, player):
    hand = game['hands'][game['index']]
    return (not game['settled'] and not game['split'] and not hand['done']
            and len(hand['cards']) == 2 and hand['cards'][0].rank == hand['cards'][1].rank
            and player.can_afford(hand['bet']))


def can_double(game, player):
    hand = game['hands'][game['index']]
    return not game['settled'] and not hand['done'] and len(hand['cards']) == 2 and player.can_afford(hand['bet'])


def split_hand(game, player):
    if not can_split(game, player):
        raise ValueError('Split için aynı değerde iki kart ve ek bahis gerekiyor.')
    hand = game['hands'][0]
    player.remove_money(hand['bet'])
    game['hands'] = [{'cards': [card, game['deck'].pop()], 'bet': hand['bet'], 'done': False}
                     for card in hand['cards']]
    game['split'] = True


def double_hand(game, player):
    if not can_double(game, player):
        raise ValueError('Double için iki kart ve ek bahis gerekiyor.')
    hand = game['hands'][game['index']]
    player.remove_money(hand['bet'])
    hand['bet'] *= 2
    hand['cards'].append(game['deck'].pop())
    hand['done'] = True
    game['double_rule'] = True
    advance_hand(game, player)


def advance_hand(game, player):
    for index, hand in enumerate(game['hands']):
        if not hand['done']:
            game['index'] = index
            return
    settle_round(game, player)


def settle_round(game, player):
    """Payouts are applied once, never from rendering a result screen."""
    if game['settled']:
        return
    if game['double_rule']:
        # Requested house rule: dealer takes exactly one extra card on Double.
        game['dealer'].append(game['deck'].pop())
    elif any(calculate_hand_value(hand['cards']) <= 21 for hand in game['hands']):
        while calculate_hand_value(game['dealer']) < 17:
            game['dealer'].append(game['deck'].pop())
    dealer = calculate_hand_value(game['dealer'])
    for hand in game['hands']:
        value = calculate_hand_value(hand['cards'])
        won = value <= 21 and (dealer > 21 or value > dealer)
        push = value <= 21 and value == dealer
        payout = hand['bet'] * 2 if won else hand['bet'] if push else 0
        if payout:
            player.add_money(payout)
        if won:
            player.casino_wins += 1
            player.add_xp(15)
        elif not push:
            player.casino_losses += 1
        game['results'].append({'outcome': 'win' if won else 'push' if push else 'loss', 'net': payout-hand['bet']})
    game['settled'] = True
    player.reduce_hunger(5)
    mark_significant_action()
    check_death_conditions()


def render_cards(cards, hidden=False):
    markup = ''
    for index, card in enumerate(cards):
        back = hidden and index > 0
        color = '#bc3445' if card.suit in ['Hearts', 'Diamonds'] else '#16242b'
        markup += (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:65px;'
                   f'height:92px;background:{"#1e4562" if back else "#fffaf0"};color:{color};'
                   'border:2px solid #c9af72;border-radius:9px;margin:4px;font-size:27px;font-weight:bold;'
                   f'box-shadow:0 5px 10px #0003">{"🂠" if back else escape(str(card))}</span>')
    st.markdown(markup, unsafe_allow_html=True)


def render_blackjack():
    render_section_header('Blackjack', '🃏')
    player = get_player()
    game = st.session_state.blackjack_state
    st.caption('Kazanma: toplam 2× ödeme · Eşitlik: iade · Split: aynı rank, el başına ayrı bahis, bir kez. '
               'Double: bahis 2×, oyuncuya tek kart; tüm eller bitince krupiyere tek ek kart (Split sonrası da ortak krupiyer eli).')
    if not game.get('active'):
        if player.money >= 10:
            bet = st.number_input('Bahis ($)', min_value=10, max_value=player.money,
                                  value=min(50, player.money), step=10, key='bj_bet_input')
            if st.button('🎲 Start Game', type='primary', use_container_width=True):
                st.session_state.blackjack_state = start_round(player, bet)
                st.rerun()
        else:
            st.warning('Blackjack için en az $10 gerekiyor.')
        if st.button('🏠 Back to Casino', use_container_width=True):
            navigate_to('casino')
        return
    st.markdown('### 🎩 Krupiyer')
    render_cards(game['dealer'], hidden=not game['settled'])
    if game['settled']:
        st.write(f"Toplam: **{calculate_hand_value(game['dealer'])}**")
    for index, hand in enumerate(game['hands']):
        active = not game['settled'] and index == game['index']
        st.markdown(f"### {'▶️' if active else '🃏'} El {index+1} · ${hand['bet']:,}")
        render_cards(hand['cards'])
        st.write(f"Toplam: **{calculate_hand_value(hand['cards'])}**")
        if game['settled']:
            result = game['results'][index]
            label = {'win': 'Kazandın', 'push': 'Eşitlik · bahis iade', 'loss': 'Kaybettin'}[result['outcome']]
            (st.success if result['outcome'] == 'win' else st.info if result['outcome'] == 'push' else st.error)(f"{label} · Net ${result['net']:+,}")
    if not game['settled']:
        hand = game['hands'][game['index']]
        hit, stand, double, split = st.columns(4)
        if hit.button('👆 Hit', use_container_width=True):
            hand['cards'].append(game['deck'].pop())
            if calculate_hand_value(hand['cards']) >= 21:
                hand['done'] = True
                advance_hand(game, player)
            st.rerun()
        if stand.button('✋ Stand', use_container_width=True):
            hand['done'] = True
            advance_hand(game, player)
            st.rerun()
        if double.button('⏫ Double', disabled=not can_double(game, player), use_container_width=True):
            double_hand(game, player)
            st.rerun()
        if split.button('✂️ Split', disabled=not can_split(game, player), use_container_width=True):
            split_hand(game, player)
            st.rerun()
    else:
        again, back = st.columns(2)
        if again.button('🔄 Play Again', use_container_width=True):
            st.session_state.blackjack_state = {}
            st.rerun()
        if back.button('🏠 Back to Casino', use_container_width=True):
            st.session_state.blackjack_state = {}
            navigate_to('casino')
