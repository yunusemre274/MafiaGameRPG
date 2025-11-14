"""Player system with stats, level, and XP tracking."""

class Player:
    def __init__(self):
        self.money = 100
        self.hp = 100
        self.max_hp = 100
        self.hunger = 100
        self.max_hunger = 100
        self.level = 1
        self.xp = 0
        self.bodyguards = 0
        self.gang_members = 0
        
        # Statistics
        self.total_actions = 0
        self.casino_wins = 0
        self.casino_losses = 0
        self.mini_games_completed = set()  # Track completed mini-games
    
    def add_xp(self, amount):
        """Add XP and check for level up."""
        self.xp += amount
        xp_needed = self.level * 100
        
        if self.xp >= xp_needed:
            self.level += 1
            self.xp -= xp_needed
            return True  # Leveled up
        return False
    
    def reduce_hunger(self, amount=5):
        """Reduce hunger by amount."""
        self.hunger = max(0, self.hunger - amount)
        self.total_actions += 1
        
        # If hunger is 0, reduce HP
        if self.hunger == 0:
            self.hp = max(0, self.hp - 10)
    
    def eat_food(self, hunger_restore):
        """Restore hunger."""
        self.hunger = min(self.max_hunger, self.hunger + hunger_restore)
    
    def take_damage(self, damage):
        """Take damage with bodyguard reduction."""
        reduced_damage = max(0, damage - (self.bodyguards * 5))
        self.hp = max(0, self.hp - reduced_damage)
        return reduced_damage
    
    def heal(self):
        """Heal to full HP."""
        self.hp = self.max_hp
    
    def is_alive(self):
        """Check if player is alive."""
        return self.hp > 0
    
    def can_afford(self, cost):
        """Check if player can afford something."""
        return self.money >= cost
    
    def add_money(self, amount):
        """Add money to player."""
        self.money += amount
    
    def remove_money(self, amount):
        """Remove money from player."""
        self.money = max(0, self.money - amount)
    
    def to_dict(self):
        """Convert player to dictionary for saving."""
        return {
            "money": self.money,
            "hp": self.hp,
            "hunger": self.hunger,
            "level": self.level,
            "xp": self.xp,
            "bodyguards": self.bodyguards,
            "gang_members": self.gang_members,
            "total_actions": self.total_actions,
            "casino_wins": self.casino_wins,
            "casino_losses": self.casino_losses,
            "mini_games_completed": list(self.mini_games_completed)
        }
    
    def from_dict(self, data):
        """Load player from dictionary."""
        self.money = data.get("money", 100)
        self.hp = data.get("hp", 100)
        self.hunger = data.get("hunger", 100)
        self.level = data.get("level", 1)
        self.xp = data.get("xp", 0)
        self.bodyguards = data.get("bodyguards", 0)
        self.gang_members = data.get("gang_members", 0)
        self.total_actions = data.get("total_actions", 0)
        self.casino_wins = data.get("casino_wins", 0)
        self.casino_losses = data.get("casino_losses", 0)
        self.mini_games_completed = set(data.get("mini_games_completed", []))
