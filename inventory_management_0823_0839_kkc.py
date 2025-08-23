# 代码生成时间: 2025-08-23 08:39:20
import sanic
from sanic.response import json

# Inventory Management System
class InventorySystem:
    def __init__(self):
        # Initialize an empty dictionary to store inventory
        self.inventory = {}

    def add_item(self, item, quantity):
        """Add an item to the inventory with the given quantity."""
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity

    def remove_item(self, item, quantity):
        """Remove an item from the inventory with the given quantity."""
        if item in self.inventory and self.inventory[item] >= quantity:
            self.inventory[item] -= quantity
            if self.inventory[item] == 0:
                del self.inventory[item]
        else:
            raise ValueError("Item not found or insufficient quantity.")

    def get_inventory(self):
        "