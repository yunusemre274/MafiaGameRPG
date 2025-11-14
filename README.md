# Casino Mafia RPG 🎰🔫

A 1D menu-based decision RPG inspired by New Star Soccer's career mode. Navigate through a criminal underworld using text menus, making strategic decisions to survive and prosper.

## 🎮 Game Features

### Core Systems
- **Player Stats**: Money, HP, Hunger, Level, XP
- **Decision-Based Gameplay**: No maps, no movement - pure menu navigation
- **Mafia System**: Extortion events, combat, and protection
- **Gang Management**: Recruit members to fight the mafia
- **Bodyguard Protection**: Hire permanent protection

### Casino Games
1. **Blackjack** - Classic card game (2x payout)
2. **Roulette** - Bet on numbers or colors (up to 35x)
3. **Dice (Zar)** - Predict dice rolls (10x for exact match)
4. **Horse Racing** - Bet on racing horses (3x payout)

### Survival Mechanics
- **Hunger System**: Must eat or lose HP
- **HP Management**: Visit hospital to heal
- **Market**: Buy food to survive
- **Death Conditions**: HP reaches 0 OR money reaches $0 with active mafia

### Progression
- **Level System**: Gain XP from actions
- **Money Thresholds**:
  - $10,000: Mafia activates
  - $25,000: Unlock Secure Building (bodyguards)
  - $50,000: Unlock Gang Building

## 🚀 How to Run

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the game:**
```bash
streamlit run main.py
```

3. **Play in your browser** - Streamlit will open automatically

## 🎯 How to Play

### Starting Out
- You begin with $100, 100 HP, and 100 Hunger
- Visit the **Market** to buy food
- Try your luck at the **Casino** to earn money
- Monitor your stats at the top panel

### Survival Tips
- Keep hunger above 0 (or you'll lose HP)
- Save money for emergencies
- Visit hospital when HP is low
- Buy food regularly from the market

### Mafia Encounters
- Mafia activates at $10,000
- Random extortion events (15% chance after actions)
- **Options**:
  - Pay: Safe but expensive
  - Reject: Fight with gang (if available) or take damage

### Combat System
- **Bodyguards**: Reduce damage by 5 HP each (never die)
- **Gang Members**: Fight mafia (die in combat)
  - Level 1-4: Lose 1 member per mafia attacker
  - Level 5+: Lose 2 members per mafia attacker

### Winning Strategy
1. Build up money through casino
2. Buy food to maintain hunger
3. Reach $25k → hire bodyguards
4. Reach $50k → build gang
5. Balance earning, spending, and survival

## 📁 Project Structure

```
casino_mafia_rpg/
├── main.py              # Entry point & navigation
├── player.py            # Player class & stats
├── game_state.py        # Session state management
├── ui_components.py     # Reusable UI elements
├── mafia.py             # Mafia events & combat
├── market.py            # Food shop
├── hospital.py          # Healing service
├── secure.py            # Bodyguard hiring
├── gang.py              # Gang recruitment
├── inventory.py         # Item management
├── save_load.py         # Save/Load system
├── sound.py             # Audio system (placeholder)
├── casino/
│   ├── blackjack.py     # Blackjack game
│   ├── roulette.py      # Roulette game
│   ├── dice.py          # Dice (Zar) game
│   └── horse_racing.py  # Horse racing game
└── requirements.txt     # Dependencies
```

## 💾 Save System

- **Save Button**: Save your progress to `savegame.json`
- **Load Button**: Resume from saved game
- Saves all stats, inventory, and progress

## 🎨 UI Features

- Gradient stat panels
- Color-coded warnings
- Responsive button layout
- Clean menu navigation
- Visual feedback for all actions

## 🔧 Technical Details

- **Framework**: Streamlit
- **Language**: Python 3.7+
- **Architecture**: Modular, menu-driven
- **State Management**: Streamlit session state
- **Save Format**: JSON

## 📝 Game Balance

### Costs
- Food: $15 - $100
- Hospital: $1,500
- Bodyguard: $5,000
- Gang Member: $3,000

### Casino Payouts
- Blackjack: 2x
- Roulette Number: 35x
- Roulette Color: 2x
- Dice Exact: 10x
- Dice Close: 3x
- Horse Racing: 3x

### XP Rewards
- Small actions: 2-5 XP
- Casino wins: 10-25 XP
- Combat survival: 30 XP
- Level up threshold: Level × 100 XP

## 🎯 Future Enhancements

- Real sound effects
- More casino games
- Additional items and boosts
- Multiple save slots
- Achievement system
- Difficulty modes

## 📄 License

This is a demonstration project. Feel free to modify and extend!

---

**Enjoy the game! Good luck surviving the mafia! 🎰🔫**
