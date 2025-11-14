# 🎮 QUICK START GUIDE

## Installation & Setup

1. **Install Python dependencies:**
   ```bash
   pip install streamlit
   ```

2. **Run the game:**
   ```bash
   streamlit run main.py
   ```

3. **The game will automatically open in your browser at:**
   - http://localhost:8501

## 🎯 First Steps

### Starting the Game
- You begin with **$100**, **100 HP**, and **100 Hunger**
- All stats are displayed at the top panel
- Navigate using the menu buttons

### Essential Actions (First 10 Minutes)

1. **Visit the Market** 🏪
   - Buy some food (Muz for $15 or Ekmek for $20)
   - Food goes into your inventory
   - Keep hunger above 50

2. **Try the Casino** 🎰
   - Start with small bets ($10-$20)
   - **Easiest game**: Dice (Zar) - bet on middle numbers (6-8)
   - **Best odds**: Blackjack (2x payout)
   - Goal: Build up to $500-$1000

3. **Use Inventory** 🎒
   - Click "Inventory" to see your items
   - Click "Use" on food to restore hunger
   - Always keep 2-3 food items on hand

### ⚠️ Important Warnings

#### Death Conditions
- **HP reaches 0** → You die
- **Hunger reaches 0** → Every action removes 10 HP
- **Money reaches $0 (after mafia activates)** → Mafia kills you

#### The $10,000 Milestone
- When you reach **$10,000**, the mafia becomes active
- Random extortion events will start occurring
- **Prepare before reaching $10k:**
  - Keep HP above 70
  - Save enough money for extortion payments
  - Consider saving the game

## 🎰 Casino Strategy Guide

### Blackjack (2x payout)
- **Hit** until you reach 17+
- **Stand** on 17-20
- Watch the dealer's visible card
- Best overall win rate

### Roulette (2x-35x payout)
- **Safe bet**: Red/Black (2x)
- **High risk**: Single number (35x)
- Best for big money quickly

### Dice/Zar (3x-10x payout)
- **Safest**: Bet on 7 (most common)
- **Good odds**: 6, 7, or 8
- Exact match = 10x
- Close (±1) = 3x

### Horse Racing (3x payout)
- Pure luck, 20% win chance
- Moderate risk, moderate reward
- Fun to watch the race

## 💰 Money Management

### Early Game ($0 - $1,000)
- Bet $10-$20 per casino game
- Buy cheapest food (Muz $15, Ekmek $20)
- Save at $500 increments

### Mid Game ($1,000 - $10,000)
- Bet $50-$100 per game
- Buy better food (Pasta $50, Pizza $100)
- **Save before reaching $10k!**

### Late Game ($10,000+)
- Mafia is active - keep $2,000+ reserve
- Aim for $25k (Bodyguards)
- Then $50k (Gang)

## 🔫 Mafia Survival Guide

### When Mafia Demands Extortion

**Option 1: PAY** (Safe)
- Lose 5-15% of your money
- No combat, no damage
- Best if you have no gang

**Option 2: REJECT** (Risky)
- Fight if you have gang members
- Take damage if you don't
- Can save money but risk HP

### Combat Mechanics

**Bodyguards** (Unlock at $25k)
- Cost: $5,000 each
- **Never die**
- Reduce damage by 5 HP per bodyguard
- Example: 3 bodyguards = -15 HP damage reduction

**Gang Members** (Unlock at $50k)
- Cost: $3,000 each
- **Fight and die in combat**
- Kill mafia members
- Loss rate:
  - Level 1-4: Lose 1 per mafia
  - Level 5+: Lose 2 per mafia

### Optimal Defense Strategy
1. Reach $25k → Buy 2-3 bodyguards
2. Reach $50k → Recruit 5-10 gang members
3. Always keep 3+ gang members
4. Bodyguards provide permanent protection

## 📊 Progression System

### Leveling Up
- Gain XP from all actions
- XP needed = Level × 100
- Higher level = better combat efficiency

### Building Unlocks
- **$25,000**: Secure Building (bodyguards)
- **$50,000**: Gang Building (gang members)

### Stats to Watch
- Keep **Hunger > 20**
- Keep **HP > 50** when possible
- Maintain **$2,000+ reserve** after mafia activates

## 💾 Save/Load Tips

- **Save often** - especially before:
  - Reaching $10k
  - Large casino bets
  - Low HP situations
- **Load** if you die or make mistakes
- Save file: `savegame.json` in game folder

## 🎯 Winning Strategy (Step-by-Step)

1. **$0 - $500**: Play Blackjack with $10-$20 bets, buy Muz
2. **$500 - $2,000**: Increase bets to $50, buy Pasta
3. **$2,000 - $5,000**: Save game, try Roulette color bets
4. **$5,000 - $10,000**: **SAVE before $10k!**, stockpile food
5. **$10,000+**: Mafia active - play conservatively
6. **$25,000**: Buy 2-3 bodyguards
7. **$50,000**: Recruit 5+ gang members
8. **$100,000+**: You've basically won!

## ⚡ Quick Tips

- **Hunger management**: Buy food every $200-$300 earned
- **HP management**: Visit hospital when HP < 50
- **Casino**: Start with small bets, increase gradually
- **Mafia**: Pay first few times, fight when strong
- **Saves**: Save every $1,000 gained
- **Death**: Don't panic - restart and try again!

## 🆘 Common Mistakes to Avoid

1. ❌ Betting all money on one game
2. ❌ Ignoring hunger until it's 0
3. ❌ Not saving before $10k
4. ❌ Fighting mafia with no gang
5. ❌ Not keeping food in inventory
6. ❌ Spending last $1,500 when HP is low

## 🎊 Enjoy the Game!

Remember: This is a **decision-based game**. Every choice matters. Balance risk and reward, manage your resources, and survive the mafia!

Good luck! 🎰🔫
