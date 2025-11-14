"""Inventory management system."""
import streamlit as st
from game_state import get_player

class InventoryItem:
    def __init__(self, name, item_type, effect_value):
        self.name = name
        self.item_type = item_type  # "food", "boost", etc.
        self.effect_value = effect_value
    
    def to_dict(self):
        return {
            "name": self.name,
            "item_type": self.item_type,
            "effect_value": self.effect_value
        }
    
    @staticmethod
    def from_dict(data):
        return InventoryItem(
            data["name"],
            data["item_type"],
            data["effect_value"]
        )

def add_to_inventory(item_name, item_type, effect_value, quantity=1):
    """Add item to inventory."""
    for _ in range(quantity):
        item = InventoryItem(item_name, item_type, effect_value)
        st.session_state.inventory.append(item)

def get_inventory_count(item_name):
    """Get count of specific item in inventory."""
    return sum(1 for item in st.session_state.inventory if item.name == item_name)

def use_item(item_name):
    """Use an item from inventory."""
    player = get_player()
    
    for i, item in enumerate(st.session_state.inventory):
        if item.name == item_name:
            # Apply effect based on item type
            if item.item_type == "food":
                player.eat_food(item.effect_value)
                st.session_state.inventory.pop(i)
                return True, f"Ate {item_name}. Restored {item.effect_value} hunger."
            break
    
    return False, "Item not found in inventory."

def get_inventory_summary():
    """Get a summary of inventory with quantities."""
    summary = {}
    for item in st.session_state.inventory:
        if item.name in summary:
            summary[item.name]["quantity"] += 1
        else:
            summary[item.name] = {
                "type": item.item_type,
                "effect": item.effect_value,
                "quantity": 1
            }
    return summary
