"""Market system for buying food and items."""
import streamlit as st
from game_state import get_player, check_death_conditions
from ui_components import render_section_header, show_success, show_error, menu_button
from inventory import add_to_inventory

# Food items available in market
FOOD_ITEMS = [
    {"name": "Muz", "price": 15, "hunger_restore": 15, "emoji": "🍌"},
    {"name": "Ekmek", "price": 20, "hunger_restore": 20, "emoji": "🍞"},
    {"name": "Simit", "price": 30, "hunger_restore": 30, "emoji": "🥯"},
    {"name": "Pasta", "price": 50, "hunger_restore": 50, "emoji": "🍝"},
    {"name": "Pizza", "price": 100, "hunger_restore": 100, "emoji": "🍕"},
]

def render_market():
    """Render the market interface."""
    from game_state import navigate_to
    
    render_section_header("Market", "🏪")
    
    player = get_player()
    
    st.markdown("### Food Shop")
    st.markdown("Buy food to restore your hunger. Carry it in your inventory!")
    
    # Display food items in columns
    cols = st.columns(3)
    
    for idx, food in enumerate(FOOD_ITEMS):
        with cols[idx % 3]:
            st.markdown(f"""
                <div style='padding: 15px; border: 2px solid #ddd; border-radius: 10px; margin: 10px 0; text-align: center;'>
                    <div style='font-size: 40px;'>{food['emoji']}</div>
                    <div style='font-weight: bold; font-size: 18px;'>{food['name']}</div>
                    <div style='color: #666;'>Price: ${food['price']}</div>
                    <div style='color: #28a745;'>+{food['hunger_restore']} Hunger</div>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Buy {food['name']}", key=f"buy_{food['name']}"):
                if player.can_afford(food['price']):
                    player.remove_money(food['price'])
                    add_to_inventory(food['name'], "food", food['hunger_restore'])
                    player.reduce_hunger(3)
                    player.add_xp(2)
                    show_success(f"Bought {food['name']} for ${food['price']}! Added to inventory.")
                    check_death_conditions()
                    st.rerun()
                else:
                    show_error(f"Not enough money! You need ${food['price']}.")
    
    st.markdown("---")
    
    if menu_button("🏠 Back to Main Menu", key="market_back"):
        navigate_to("main_menu")
