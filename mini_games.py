"""Safe mini-games for earning money through skill and logic."""
import streamlit as st
import random
from game_state import get_player, navigate_to
from ui_components import render_section_header, show_success, show_error, show_info

def render_mini_games():
    """Main mini-games hub."""
    render_section_header("💼 Street Jobs", "💰")
    
    player = get_player()
    
    st.markdown("""
    ### Need Money? Try These Jobs!
    Earn guaranteed money through skill-based tasks. No gambling, just hard work!
    """)
    
    st.markdown(f"**Your Money: ${player.money}**")
    st.markdown("---")
    
    # Game selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎴 Card Memory")
        st.markdown("Match pairs of cards")
        if "card_memory" in player.mini_games_completed:
            st.markdown("**✅ COMPLETED**")
            st.button("Play Card Memory", use_container_width=True, disabled=True, key="cm_disabled")
        else:
            st.markdown("**Reward: $50**")
            if st.button("Play Card Memory", use_container_width=True):
                st.session_state.current_minigame = "card_memory"
                st.rerun()
    
    with col2:
        st.markdown("### 🔢 Math Challenge")
        st.markdown("Solve quick math problems")
        if "math_challenge" in player.mini_games_completed:
            st.markdown("**✅ COMPLETED**")
            st.button("Play Math Challenge", use_container_width=True, disabled=True, key="mc_disabled")
        else:
            st.markdown("**Reward: $30**")
            if st.button("Play Math Challenge", use_container_width=True):
                st.session_state.current_minigame = "math_challenge"
                st.rerun()
    
    with col3:
        st.markdown("### 🎯 Pattern Memory")
        st.markdown("Remember the sequence")
        if "pattern_memory" in player.mini_games_completed:
            st.markdown("**✅ COMPLETED**")
            st.button("Play Pattern Memory", use_container_width=True, disabled=True, key="pm_disabled")
        else:
            st.markdown("**Reward: $40**")
            if st.button("Play Pattern Memory", use_container_width=True):
                st.session_state.current_minigame = "pattern_memory"
                st.rerun()
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧩 Code Breaker")
        st.markdown("Crack the secret code")
        if "code_breaker" in player.mini_games_completed:
            st.markdown("**✅ COMPLETED**")
            st.button("Play Code Breaker", use_container_width=True, disabled=True, key="cb_disabled")
        else:
            st.markdown("**Reward: $60**")
            if st.button("Play Code Breaker", use_container_width=True):
                st.session_state.current_minigame = "code_breaker"
                st.rerun()
    
    with col2:
        st.markdown("### 🎲 Number Guesser")
        st.markdown("Find the hidden number")
        if "number_guesser" in player.mini_games_completed:
            st.markdown("**✅ COMPLETED**")
            st.button("Play Number Guesser", use_container_width=True, disabled=True, key="ng_disabled")
        else:
            st.markdown("**Reward: $35**")
            if st.button("Play Number Guesser", use_container_width=True):
                st.session_state.current_minigame = "number_guesser"
                st.rerun()
    
    st.markdown("---")
    
    if st.button("🏠 Back to Main Menu", use_container_width=True):
        navigate_to("main")

def render_card_memory():
    """Card matching memory game."""
    render_section_header("🎴 Card Memory Game", "💰")
    
    player = get_player()
    
    # Initialize game
    if 'cm_cards' not in st.session_state:
        symbols = ['🎭', '🎨', '🎪', '🎬', '🎸', '🎺', '🎹', '🎤']
        cards = symbols + symbols
        random.shuffle(cards)
        st.session_state.cm_cards = cards
        st.session_state.cm_revealed = [False] * 16
        st.session_state.cm_matched = [False] * 16
        st.session_state.cm_first_pick = None
        st.session_state.cm_second_pick = None
        st.session_state.cm_attempts = 0
        st.session_state.cm_completed = False
    
    st.markdown("**Match all pairs of cards to win $50!**")
    st.markdown(f"**Attempts: {st.session_state.cm_attempts}**")
    st.markdown("---")
    
    # Check if second card was picked (need to hide them)
    if st.session_state.cm_second_pick is not None:
        idx1 = st.session_state.cm_first_pick
        idx2 = st.session_state.cm_second_pick
        
        if st.session_state.cm_cards[idx1] == st.session_state.cm_cards[idx2]:
            st.session_state.cm_matched[idx1] = True
            st.session_state.cm_matched[idx2] = True
            show_success("Match found! ✨")
        else:
            st.session_state.cm_revealed[idx1] = False
            st.session_state.cm_revealed[idx2] = False
        
        st.session_state.cm_first_pick = None
        st.session_state.cm_second_pick = None
    
    # Check if game completed
    if all(st.session_state.cm_matched) and not st.session_state.cm_completed:
        st.session_state.cm_completed = True
        player.add_money(50)
        player.add_xp(10)
        player.mini_games_completed.add("card_memory")
        show_success(f"🎉 You won $50! (Completed in {st.session_state.cm_attempts} attempts)")
    
    # Display cards in 4x4 grid
    for row in range(4):
        cols = st.columns(4)
        for col_idx in range(4):
            idx = row * 4 + col_idx
            with cols[col_idx]:
                if st.session_state.cm_matched[idx]:
                    st.markdown(f"<div style='text-align: center; font-size: 50px;'>{st.session_state.cm_cards[idx]}</div>", unsafe_allow_html=True)
                elif st.session_state.cm_revealed[idx]:
                    st.markdown(f"<div style='text-align: center; font-size: 50px;'>{st.session_state.cm_cards[idx]}</div>", unsafe_allow_html=True)
                else:
                    if st.button("🎴", key=f"card_{idx}", use_container_width=True):
                        if st.session_state.cm_first_pick is None:
                            st.session_state.cm_first_pick = idx
                            st.session_state.cm_revealed[idx] = True
                            st.rerun()
                        elif st.session_state.cm_second_pick is None and idx != st.session_state.cm_first_pick:
                            st.session_state.cm_second_pick = idx
                            st.session_state.cm_revealed[idx] = True
                            st.session_state.cm_attempts += 1
                            st.rerun()
    
    st.markdown("---")
    
    if st.session_state.cm_completed:
        if st.button("🏠 Back to Jobs", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith('cm_'):
                    del st.session_state[key]
            st.session_state.current_minigame = None
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Restart Game", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('cm_'):
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to Jobs", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('cm_'):
                        del st.session_state[key]
                st.session_state.current_minigame = None
                st.rerun()

def render_math_challenge():
    """Quick math problem solving game."""
    render_section_header("🔢 Math Challenge", "💰")
    
    player = get_player()
    
    # Initialize game
    if 'mc_problems' not in st.session_state:
        st.session_state.mc_problems = []
        st.session_state.mc_current = 0
        st.session_state.mc_score = 0
        st.session_state.mc_total = 5
        
        # Generate 5 problems
        for _ in range(5):
            op = random.choice(['+', '-', '*'])
            if op == '+':
                a, b = random.randint(10, 50), random.randint(10, 50)
                answer = a + b
            elif op == '-':
                a, b = random.randint(20, 80), random.randint(10, 50)
                answer = a - b
            else:  # *
                a, b = random.randint(2, 15), random.randint(2, 15)
                answer = a * b
            
            st.session_state.mc_problems.append({
                'a': a, 'b': b, 'op': op, 'answer': answer
            })
    
    if st.session_state.mc_current < st.session_state.mc_total:
        problem = st.session_state.mc_problems[st.session_state.mc_current]
        
        st.markdown(f"**Question {st.session_state.mc_current + 1} of {st.session_state.mc_total}**")
        st.markdown(f"**Score: {st.session_state.mc_score}/{st.session_state.mc_current}**")
        st.markdown("---")
        
        st.markdown(f"### What is {problem['a']} {problem['op']} {problem['b']}?")
        
        answer = st.number_input("Your answer:", value=0, step=1, key=f"mc_answer_{st.session_state.mc_current}")
        
        if st.button("Submit Answer", use_container_width=True):
            if answer == problem['answer']:
                st.session_state.mc_score += 1
                show_success("Correct! ✅")
            else:
                show_error(f"Wrong! The answer was {problem['answer']}")
            
            st.session_state.mc_current += 1
            st.rerun()
    
    else:
        # Game completed
        st.markdown("### 🎯 Challenge Complete!")
        st.markdown(f"**Final Score: {st.session_state.mc_score}/{st.session_state.mc_total}**")
        
        if st.session_state.mc_score >= 3:
            reward = st.session_state.mc_score * 10
            show_success(f"Well done! You earned ${reward}!")
            player.add_money(reward)
            player.add_xp(5)
            player.mini_games_completed.add("math_challenge")
        else:
            show_error("You need at least 3 correct answers to earn money. Try again!")
        
        st.markdown("---")
        
        if st.session_state.mc_score >= 3:
            if st.button("🏠 Back to Jobs", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('mc_'):
                        del st.session_state[key]
                st.session_state.current_minigame = None
                st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Try Again", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith('mc_'):
                            del st.session_state[key]
                    st.rerun()
            
            with col2:
                if st.button("🏠 Back to Jobs", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith('mc_'):
                            del st.session_state[key]
                    st.session_state.current_minigame = None
                    st.rerun()

def render_pattern_memory():
    """Pattern sequence memory game."""
    render_section_header("🎯 Pattern Memory", "💰")
    
    player = get_player()
    
    # Initialize game
    if 'pm_pattern' not in st.session_state:
        st.session_state.pm_pattern = [random.randint(0, 3) for _ in range(4)]
        st.session_state.pm_user_input = []
        st.session_state.pm_showing = True
        st.session_state.pm_completed = False
    
    colors = ['🔴', '🔵', '🟢', '🟡']
    color_names = ['Red', 'Blue', 'Green', 'Yellow']
    
    if st.session_state.pm_showing:
        st.markdown("### Memorize this pattern!")
        pattern_display = " → ".join([colors[i] for i in st.session_state.pm_pattern])
        st.markdown(f"<div style='text-align: center; font-size: 60px;'>{pattern_display}</div>", unsafe_allow_html=True)
        
        if st.button("✅ I've Memorized It!", use_container_width=True):
            st.session_state.pm_showing = False
            st.rerun()
    
    else:
        st.markdown("### Now enter the pattern!")
        
        if st.session_state.pm_user_input:
            user_display = " → ".join([colors[i] for i in st.session_state.pm_user_input])
            st.markdown(f"**Your input:** {user_display}")
        else:
            st.markdown("**Your input:** (none yet)")
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        for idx, col in enumerate([col1, col2, col3, col4]):
            with col:
                if st.button(f"{colors[idx]} {color_names[idx]}", use_container_width=True, key=f"color_{idx}"):
                    st.session_state.pm_user_input.append(idx)
                    
                    if len(st.session_state.pm_user_input) == len(st.session_state.pm_pattern):
                        # Check if correct
                        if st.session_state.pm_user_input == st.session_state.pm_pattern:
                            st.session_state.pm_completed = True
                            player.add_money(40)
                            player.add_xp(8)
                            player.mini_games_completed.add("pattern_memory")
                            show_success("Perfect! You earned $40! 🎉")
                        else:
                            show_error("Wrong pattern! Try again.")
                            st.session_state.pm_user_input = []
                    
                    st.rerun()
        
        st.markdown("---")
        
        if st.session_state.pm_completed:
            if st.button("🏠 Back to Jobs", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('pm_'):
                        del st.session_state[key]
                st.session_state.current_minigame = None
                st.rerun()
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Clear Input", use_container_width=True):
                    st.session_state.pm_user_input = []
                    st.rerun()
            
            with col2:
                if st.button("👁️ Show Pattern Again", use_container_width=True):
                    st.session_state.pm_showing = True
                    st.rerun()
            
            with col3:
                if st.button("🏠 Back to Jobs", use_container_width=True):
                    for key in list(st.session_state.keys()):
                        if key.startswith('pm_'):
                            del st.session_state[key]
                    st.session_state.current_minigame = None
                    st.rerun()

def render_code_breaker():
    """Code breaking logic game."""
    render_section_header("🧩 Code Breaker", "💰")
    
    player = get_player()
    
    # Initialize game
    if 'cb_code' not in st.session_state:
        st.session_state.cb_code = [random.randint(1, 6) for _ in range(4)]
        st.session_state.cb_attempts = []
        st.session_state.cb_max_attempts = 8
        st.session_state.cb_won = False
    
    st.markdown("""
    **Crack the 4-digit code! (Numbers 1-6)**
    - 🟢 = Correct number in correct position
    - 🟡 = Correct number in wrong position
    - ⚫ = Wrong number
    """)
    
    st.markdown(f"**Attempts left: {st.session_state.cb_max_attempts - len(st.session_state.cb_attempts)}**")
    st.markdown("---")
    
    if not st.session_state.cb_won and len(st.session_state.cb_attempts) < st.session_state.cb_max_attempts:
        # Input section
        cols = st.columns(4)
        guess = []
        for i, col in enumerate(cols):
            with col:
                num = st.selectbox(f"Digit {i+1}", options=[1,2,3,4,5,6], key=f"cb_digit_{i}")
                guess.append(num)
        
        if st.button("🔍 Try This Code", use_container_width=True):
            # Check the guess
            feedback = []
            code_copy = st.session_state.cb_code.copy()
            guess_copy = guess.copy()
            
            # First pass: check exact matches
            for i in range(4):
                if guess[i] == st.session_state.cb_code[i]:
                    feedback.append('🟢')
                    code_copy[i] = None
                    guess_copy[i] = None
            
            # Second pass: check wrong position
            for i in range(4):
                if guess_copy[i] is not None and guess_copy[i] in code_copy:
                    feedback.append('🟡')
                    code_copy[code_copy.index(guess_copy[i])] = None
            
            # Fill remaining with wrong
            while len(feedback) < 4:
                feedback.append('⚫')
            
            st.session_state.cb_attempts.append({
                'guess': guess,
                'feedback': feedback
            })
            
            # Check if won
            if feedback.count('🟢') == 4:
                st.session_state.cb_won = True
                reward = 60 + (st.session_state.cb_max_attempts - len(st.session_state.cb_attempts)) * 5
                player.add_money(reward)
                player.add_xp(15)
                player.mini_games_completed.add("code_breaker")
                show_success(f"🎉 Code cracked! You earned ${reward}!")
            
            st.rerun()
    
    # Show previous attempts
    if st.session_state.cb_attempts:
        st.markdown("### Previous Attempts:")
        for i, attempt in enumerate(st.session_state.cb_attempts):
            guess_str = " ".join(str(x) for x in attempt['guess'])
            feedback_str = " ".join(attempt['feedback'])
            st.markdown(f"**{i+1}.** {guess_str} → {feedback_str}")
    
    # Game over
    if st.session_state.cb_won:
        st.markdown("---")
        st.markdown("### 🎉 You cracked the code!")
    elif len(st.session_state.cb_attempts) >= st.session_state.cb_max_attempts:
        code_str = " ".join(str(x) for x in st.session_state.cb_code)
        show_error(f"Out of attempts! The code was: {code_str}")
    
    st.markdown("---")
    
    if st.session_state.cb_won:
        if st.button("🏠 Back to Jobs", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith('cb_'):
                    del st.session_state[key]
            st.session_state.current_minigame = None
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Code", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('cb_'):
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to Jobs", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('cb_'):
                        del st.session_state[key]
                st.session_state.current_minigame = None
                st.rerun()

def render_number_guesser():
    """Number guessing game."""
    render_section_header("🎲 Number Guesser", "💰")
    
    player = get_player()
    
    # Initialize game
    if 'ng_number' not in st.session_state:
        st.session_state.ng_number = random.randint(1, 100)
        st.session_state.ng_attempts = 0
        st.session_state.ng_max_attempts = 7
        st.session_state.ng_won = False
        st.session_state.ng_history = []
    
    st.markdown("**Guess the number between 1 and 100!**")
    st.markdown(f"**Attempts left: {st.session_state.ng_max_attempts - st.session_state.ng_attempts}**")
    st.markdown("---")
    
    if not st.session_state.ng_won and st.session_state.ng_attempts < st.session_state.ng_max_attempts:
        guess = st.number_input("Your guess:", min_value=1, max_value=100, value=50, step=1)
        
        if st.button("🎯 Submit Guess", use_container_width=True):
            st.session_state.ng_attempts += 1
            
            if guess == st.session_state.ng_number:
                st.session_state.ng_won = True
                reward = 35 + (st.session_state.ng_max_attempts - st.session_state.ng_attempts) * 5
                player.add_money(reward)
                player.add_xp(7)
                player.mini_games_completed.add("number_guesser")
                show_success(f"🎉 Correct! You earned ${reward}!")
                st.session_state.ng_history.append(f"{guess} ✅ CORRECT!")
            elif guess < st.session_state.ng_number:
                st.session_state.ng_history.append(f"{guess} ⬆️ Too low")
                show_info("Too low! Try higher.")
            else:
                st.session_state.ng_history.append(f"{guess} ⬇️ Too high")
                show_info("Too high! Try lower.")
            
            st.rerun()
    
    # Show history
    if st.session_state.ng_history:
        st.markdown("### Guess History:")
        for entry in st.session_state.ng_history:
            st.markdown(f"- {entry}")
    
    # Game over
    if not st.session_state.ng_won and st.session_state.ng_attempts >= st.session_state.ng_max_attempts:
        show_error(f"Out of attempts! The number was: {st.session_state.ng_number}")
    
    st.markdown("---")
    
    if st.session_state.ng_won:
        if st.button("🏠 Back to Jobs", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key.startswith('ng_'):
                    del st.session_state[key]
            st.session_state.current_minigame = None
            st.rerun()
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Number", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('ng_'):
                        del st.session_state[key]
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to Jobs", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key.startswith('ng_'):
                        del st.session_state[key]
                st.session_state.current_minigame = None
                st.rerun()
