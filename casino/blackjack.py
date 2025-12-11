"""Blackjack casino game."""
import streamlit as st
import random
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action
from ui_components import render_section_header, show_success, show_error, show_info, render_money_bar

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    
    def value(self):
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def __str__(self):
        suits = {'Hearts': '♥️', 'Diamonds': '♦️', 'Clubs': '♣️', 'Spades': '♠️'}
        return f"{self.rank}{suits[self.suit]}"

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [Card(suit, rank) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = sum(card.value() for card in hand)
    aces = sum(1 for card in hand if card.rank == 'A')
    
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    
    return value

def render_blackjack():
    """Render the blackjack game."""
    render_section_header("Blackjack", "🃏")
    
    player = get_player()
    
    # Always show money bar
    render_money_bar()
    
    # Initialize game state
    if 'bj_game_active' not in st.session_state:
        st.session_state.bj_game_active = False
        st.session_state.bj_bet = 0
        st.session_state.bj_deck = []
        st.session_state.bj_player_hand = []
        st.session_state.bj_dealer_hand = []
        st.session_state.bj_game_over = False
        st.session_state.bj_result = ""
    
    if not st.session_state.bj_game_active:
        st.markdown("### Place Your Bet")
        
        # Check if player has enough money
        if player.money < 10:
            st.warning("💸 You need at least $10 to play Blackjack! Try Street Jobs to earn some money.")
            if st.button("🏠 Back to Casino", use_container_width=True):
                navigate_to("casino")
            return
        
        bet_amount = st.number_input(
            "Enter bet amount:",
            min_value=10,
            max_value=player.money,
            value=min(50, player.money),
            step=10,
            key="bj_bet_input"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎲 Start Game", use_container_width=True):
                st.session_state.bj_bet = bet_amount
                player.remove_money(bet_amount)  # Deduct bet upfront
                st.session_state.bj_deck = create_deck()
                st.session_state.bj_player_hand = [st.session_state.bj_deck.pop(), st.session_state.bj_deck.pop()]
                st.session_state.bj_dealer_hand = [st.session_state.bj_deck.pop(), st.session_state.bj_deck.pop()]
                st.session_state.bj_game_active = True
                st.session_state.bj_game_over = False
                player.reduce_hunger(5)
                mark_significant_action()  # Mark for mafia event check
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to Casino", use_container_width=True):
                navigate_to("casino")
    
    else:
        # Game is active
        player_value = calculate_hand_value(st.session_state.bj_player_hand)
        dealer_value = calculate_hand_value(st.session_state.bj_dealer_hand)
        
        st.markdown(f"**Current Bet: ${st.session_state.bj_bet}**")
        
        # Display dealer's hand
        st.markdown("### 🎩 Dealer's Hand")
        if st.session_state.bj_game_over:
            dealer_cards = " ".join([str(card) for card in st.session_state.bj_dealer_hand])
            st.markdown(f"<div style='font-size: 40px;'>{dealer_cards}</div>", unsafe_allow_html=True)
            st.markdown(f"**Value: {dealer_value}**")
        else:
            visible_card = str(st.session_state.bj_dealer_hand[0])
            st.markdown(f"<div style='font-size: 40px;'>{visible_card} 🎴</div>", unsafe_allow_html=True)
            st.markdown("**Value: ??**")
        
        # Display player's hand
        st.markdown("### 🎮 Your Hand")
        player_cards = " ".join([str(card) for card in st.session_state.bj_player_hand])
        st.markdown(f"<div style='font-size: 40px;'>{player_cards}</div>", unsafe_allow_html=True)
        st.markdown(f"**Value: {player_value}**")
        
        if not st.session_state.bj_game_over:
            if player_value > 21:
                st.session_state.bj_game_over = True
                st.session_state.bj_result = "bust"
                st.rerun()
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("👆 Hit", use_container_width=True):
                        st.session_state.bj_player_hand.append(st.session_state.bj_deck.pop())
                        st.rerun()
                
                with col2:
                    if st.button("✋ Stand", use_container_width=True):
                        # Dealer plays
                        while calculate_hand_value(st.session_state.bj_dealer_hand) < 17:
                            st.session_state.bj_dealer_hand.append(st.session_state.bj_deck.pop())
                        
                        dealer_value = calculate_hand_value(st.session_state.bj_dealer_hand)
                        
                        if dealer_value > 21:
                            st.session_state.bj_result = "dealer_bust"
                        elif dealer_value > player_value:
                            st.session_state.bj_result = "dealer_win"
                        elif dealer_value < player_value:
                            st.session_state.bj_result = "player_win"
                        else:
                            st.session_state.bj_result = "push"
                        
                        st.session_state.bj_game_over = True
                        st.rerun()
        
        else:
            # Game over, show result
            st.markdown("---")
            
            if st.session_state.bj_result == "bust":
                show_error(f"BUST! You lost ${st.session_state.bj_bet}!")
                player.casino_losses += 1
            elif st.session_state.bj_result == "dealer_bust":
                winnings = st.session_state.bj_bet * 2  # Return bet + bet profit
                show_success(f"Dealer BUST! You won ${st.session_state.bj_bet} profit!")
                player.add_money(winnings)
                player.casino_wins += 1
                player.add_xp(15)
            elif st.session_state.bj_result == "player_win":
                winnings = st.session_state.bj_bet * 2  # Return bet + bet profit
                show_success(f"You WIN! Won ${st.session_state.bj_bet} profit!")
                player.add_money(winnings)
                player.casino_wins += 1
                player.add_xp(15)
            elif st.session_state.bj_result == "dealer_win":
                show_error(f"Dealer wins. You lost ${st.session_state.bj_bet}!")
                player.casino_losses += 1
            else:  # push
                show_info("PUSH! Bet returned.")
                player.add_money(st.session_state.bj_bet)  # Return bet on push
            
            check_death_conditions()
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Play Again", use_container_width=True):
                    st.session_state.bj_game_active = False
                    st.rerun()
            
            with col2:
                if st.button("🏠 Back to Casino", use_container_width=True):
                    st.session_state.bj_game_active = False
                    navigate_to("casino")
