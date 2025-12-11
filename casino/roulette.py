"""Roulette casino game with 2D table, wheel animation, and chip betting."""
import streamlit as st
import random
import time
from game_state import get_player, check_death_conditions, navigate_to, mark_significant_action

# Roulette wheel layout
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]

# Chip definitions
CHIPS = [
    {"value": 10, "emoji": "⚪", "name": "$10"},
    {"value": 20, "emoji": "🟡", "name": "$20"},
    {"value": 50, "emoji": "🔴", "name": "$50"},
    {"value": 100, "emoji": "🔵", "name": "$100"},
    {"value": 1000, "emoji": "🟢", "name": "$1K"},
    {"value": 5000, "emoji": "🟣", "name": "$5K"},
    {"value": 10000, "emoji": "⚫", "name": "$10K"},
]

def init_roulette_state():
    """Initialize roulette game state."""
    if 'roulette_bet_amount' not in st.session_state:
        st.session_state.roulette_bet_amount = 0
    if 'roulette_bet_type' not in st.session_state:
        st.session_state.roulette_bet_type = None
    if 'roulette_bet_choice' not in st.session_state:
        st.session_state.roulette_bet_choice = None
    if 'roulette_selected_chip' not in st.session_state:
        st.session_state.roulette_selected_chip = 10
    if 'roulette_result' not in st.session_state:
        st.session_state.roulette_result = None
    if 'roulette_result_number' not in st.session_state:
        st.session_state.roulette_result_number = None
    if 'roulette_show_result' not in st.session_state:
        st.session_state.roulette_show_result = False

def render_balance_banner():
    """Render balance display."""
    player = get_player()
    st.success(f"🪙 **Balance: ${player.money:,}** 🪙")

def render_chips():
    """Render chip selection buttons."""
    player = get_player()
    
    st.subheader("🎟️ Select Chip Value")
    
    cols = st.columns(len(CHIPS))
    for i, chip in enumerate(CHIPS):
        with cols[i]:
            disabled = player.money < chip["value"]
            selected = st.session_state.roulette_selected_chip == chip["value"]
            
            label = f"{chip['emoji']} {chip['name']}"
            if selected:
                label = f"✓ {label}"
            
            if st.button(label, key=f"chip_{chip['value']}", disabled=disabled, use_container_width=True):
                st.session_state.roulette_selected_chip = chip["value"]
                st.rerun()

def render_roulette_table():
    """Render the 2D roulette betting table."""
    st.subheader("🎰 Roulette Table - Click to Place Bet")
    
    current_bet = st.session_state.roulette_bet_amount
    bet_type = st.session_state.roulette_bet_type
    bet_choice = st.session_state.roulette_bet_choice
    
    if current_bet > 0:
        st.info(f"💰 **Current Bet: ${current_bet:,}** on **{bet_type}: {bet_choice}**")
    
    # Zero
    if st.button("🟢 0 (Zero)", key="num_0", use_container_width=True):
        place_bet("Number", 0)
    
    st.write("**Numbers:**")
    
    # Row 1
    row1_cols = st.columns(12)
    row1_nums = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
    for i, num in enumerate(row1_nums):
        with row1_cols[i]:
            color = "🔴" if num in RED_NUMBERS else "⚫"
            if st.button(f"{color}{num}", key=f"num_{num}"):
                place_bet("Number", num)
    
    # Row 2
    row2_cols = st.columns(12)
    row2_nums = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
    for i, num in enumerate(row2_nums):
        with row2_cols[i]:
            color = "🔴" if num in RED_NUMBERS else "⚫"
            if st.button(f"{color}{num}", key=f"num_{num}"):
                place_bet("Number", num)
    
    # Row 3
    row3_cols = st.columns(12)
    row3_nums = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
    for i, num in enumerate(row3_nums):
        with row3_cols[i]:
            color = "🔴" if num in RED_NUMBERS else "⚫"
            if st.button(f"{color}{num}", key=f"num_{num}"):
                place_bet("Number", num)
    
    st.write("**Outside Bets:**")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔴 RED", key="bet_red", use_container_width=True):
            place_bet("Color", "Red")
    
    with col2:
        if st.button("⚫ BLACK", key="bet_black", use_container_width=True):
            place_bet("Color", "Black")
    
    with col3:
        if st.button("🔢 EVEN", key="bet_even", use_container_width=True):
            place_bet("Parity", "Even")
    
    with col4:
        if st.button("🔢 ODD", key="bet_odd", use_container_width=True):
            place_bet("Parity", "Odd")

def place_bet(bet_type, bet_choice):
    """Place a bet on the table."""
    player = get_player()
    chip_value = st.session_state.roulette_selected_chip
    
    if player.money < chip_value:
        st.warning("💸 Not enough money for this chip!")
        return
    
    st.session_state.roulette_bet_amount = chip_value
    st.session_state.roulette_bet_type = bet_type
    st.session_state.roulette_bet_choice = bet_choice
    st.rerun()

def render_wheel(result_number=None):
    """Render the roulette wheel result."""
    if result_number is not None:
        if result_number == 0:
            color = "🟢"
            color_name = "Green"
        elif result_number in RED_NUMBERS:
            color = "🔴"
            color_name = "Red"
        else:
            color = "⚫"
            color_name = "Black"
        
        st.subheader("🎡 Last Result")
        st.metric(label="Winning Number", value=f"{color} {result_number}", delta=color_name)

def handle_spin():
    """Handle the spin button and game logic."""
    player = get_player()
    
    bet_amount = st.session_state.roulette_bet_amount
    bet_type = st.session_state.roulette_bet_type
    bet_choice = st.session_state.roulette_bet_choice
    
    if bet_amount <= 0 or bet_type is None:
        st.warning("⚠️ Please place a bet first by selecting a chip and clicking on the table!")
        return False
    
    if player.money < bet_amount:
        st.warning("💸 Not enough money for this bet!")
        return False
    
    # Deduct bet
    player.remove_money(bet_amount)
    
    # Spin animation
    spin_placeholder = st.empty()
    
    for i in range(12):
        random_num = random.randint(0, 36)
        color = "🟢" if random_num == 0 else "🔴" if random_num in RED_NUMBERS else "⚫"
        spin_placeholder.header(f"🎡 Spinning... {color} {random_num}")
        time.sleep(0.15 + (i * 0.03))
    
    # Final result
    result_number = random.randint(0, 36)
    result_color = "Green" if result_number == 0 else "Red" if result_number in RED_NUMBERS else "Black"
    result_parity = "Zero" if result_number == 0 else "Even" if result_number % 2 == 0 else "Odd"
    
    color_emoji = "🟢" if result_number == 0 else "🔴" if result_number in RED_NUMBERS else "⚫"
    spin_placeholder.header(f"🎯 Result: {color_emoji} {result_number} ({result_color})")
    
    # Check win
    won = False
    
    if bet_type == "Number":
        won = (bet_choice == result_number)
    elif bet_type == "Color":
        won = (bet_choice == result_color)
    elif bet_type == "Parity":
        won = (bet_choice == result_parity)
    
    player.reduce_hunger(5)
    mark_significant_action()
    
    st.session_state.roulette_result_number = result_number
    
    if won:
        winnings = bet_amount * 2
        profit = bet_amount
        player.add_money(winnings)
        player.casino_wins += 1
        player.add_xp(20)
        
        st.session_state.roulette_result = "win"
        st.session_state.roulette_win_amount = profit
    else:
        player.casino_losses += 1
        st.session_state.roulette_result = "lose"
        st.session_state.roulette_lose_amount = bet_amount
    
    st.session_state.roulette_bet_amount = 0
    st.session_state.roulette_bet_type = None
    st.session_state.roulette_bet_choice = None
    st.session_state.roulette_show_result = True
    
    check_death_conditions()
    
    return True

def render_result_screen():
    """Render win/lose result screen."""
    result = st.session_state.roulette_result
    result_number = st.session_state.roulette_result_number
    
    color_emoji = "🟢" if result_number == 0 else "🔴" if result_number in RED_NUMBERS else "⚫"
    
    if result == "win":
        win_amount = st.session_state.get('roulette_win_amount', 0)
        st.balloons()
        st.success(f"""
        ## 🎉 YOU WIN! 🎉
        
        **Winning Number:** {color_emoji} {result_number}
        
        **Profit:** +${win_amount:,}
        """)
    else:
        lose_amount = st.session_state.get('roulette_lose_amount', 0)
        st.error(f"""
        ## 😔 YOU LOST
        
        **Winning Number:** {color_emoji} {result_number}
        
        **Lost:** -${lose_amount:,}
        """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Play Again", key="roulette_play_again", use_container_width=True):
            st.session_state.roulette_show_result = False
            st.session_state.roulette_result = None
            st.rerun()
    with col2:
        if st.button("🏠 Back to Casino", key="roulette_back_casino", use_container_width=True):
            st.session_state.roulette_show_result = False
            st.session_state.roulette_result = None
            navigate_to("casino")

def render_roulette():
    """Main roulette game renderer."""
    st.title("🎡 ROULETTE")
    
    init_roulette_state()
    
    player = get_player()
    
    render_balance_banner()
    
    # Check if player has enough money
    if player.money < 10:
        st.warning("💸 You need at least $10 to play Roulette! Try Street Jobs to earn some money.")
        if st.button("🏠 Back to Casino", key="roulette_back_no_money", use_container_width=True):
            navigate_to("casino")
        return
    
    if st.session_state.roulette_show_result:
        render_result_screen()
        return
    
    # Show last result if any
    if st.session_state.roulette_result_number is not None:
        render_wheel(st.session_state.roulette_result_number)
    
    st.divider()
    
    render_chips()
    
    st.divider()
    
    render_roulette_table()
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎰 SPIN THE WHEEL!", key="roulette_spin_wheel", use_container_width=True, type="primary"):
            handle_spin()
            st.rerun()
    
    if st.session_state.roulette_bet_amount > 0:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🗑️ Clear Bet", key="roulette_clear_bet", use_container_width=True):
                st.session_state.roulette_bet_amount = 0
                st.session_state.roulette_bet_type = None
                st.session_state.roulette_bet_choice = None
                st.rerun()
    
    st.divider()
    
    if st.button("🏠 Back to Casino", key="roulette_back_to_casino", use_container_width=True):
        navigate_to("casino")
