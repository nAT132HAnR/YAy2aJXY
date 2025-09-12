# 代码生成时间: 2025-09-12 19:29:09
from sanic import Sanic
from sanic.response import json, text
from sanic.exceptions import ServerError, NotFound, BadRequest
import uuid

# Inventory item data model
class InventoryItem:
    def __init__(self, name, quantity):
        self.id = str(uuid.uuid4())  # Unique identifier
        self.name = name
        self.quantity = quantity

    def update_quantity(self, change):
        self.quantity += change
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")

# Inventory manager
class InventoryManager:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.id] = item

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
        else:
            raise NotFound("Item not found")

    def update_item(self, item_id, quantity):
        if item_id in self.items:
            try:
                self.items[item_id].update_quantity(quantity)
            except ValueError as e:
                raise ServerError(e)
        else:
            raise NotFound("Item not found")

    def get_item(self, item_id):
        if item_id in self.items:
            return self.items[item_id]
        else:
            raise NotFound("Item not found")

# Sanic application
app = Sanic("Inventory Management")
inventory = InventoryManager()

# Add new item endpoint
@app.post("/item")
async def add_item(request):
    item_name = request.json.get("name")
    item_quantity = request.json.get("quantity")
    if item_name is None or item_quantity is None:
        raise BadRequest("Missing name or quantity")
    item = InventoryItem(item_name, item_quantity)
    inventory.add_item(item)
    return json(item.__dict__)

# Update item endpoint
@app.put("/item/<item_id>")
async def update_item(request, item_id):
    item_quantity = request.json.get("quantity")
    if item_quantity is None:
        raise BadRequest("Missing quantity")
    try:
        inventory.update_item(item_id, item_quantity)
    except NotFound:
        return text("Item not found", status=404)
    except ServerError as e:
        return text(str(e), status=500)
    item = inventory.get_item(item_id)
    return json(item.__dict__)

# Get item endpoint
@app.get("/item/<item_id>")
async def get_item(request, item_id):
    try:
        item = inventory.get_item(item_id)
    except NotFound:
        return text("Item not found", status=404)
    return json(item.__dict__)

# Remove item endpoint
@app.delete("/item/<item_id>")
async def remove_item(request, item_id):
    try:
        inventory.remove_item(item_id)
    except NotFound:
        return text("Item not found", status=404)
    return text("Item removed successfully")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)