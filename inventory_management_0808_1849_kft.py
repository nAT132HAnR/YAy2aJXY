# 代码生成时间: 2025-08-08 18:49:48
from sanic import Sanic, response, exceptions
from sanic.request import Request
from sanic.response import json
from sanic_cors import CORS
import uuid
import json

# Initialize the Sanic app
app = Sanic("InventoryManagement")
CORS(app)  # Enable CORS for all origins

# In-memory storage for inventory items
inventory = {}

# Inventory API routes
@app.route("/items", methods=["GET"])
async def list_items(request: Request):
    """
    List all items in the inventory.
    """
    return response.json(inventory)

@app.route("/items/<item_id:str>", methods=["GET"])
async def get_item(request: Request, item_id: str):
    """
    Get a single item from the inventory by its ID.
    """
    item = inventory.get(item_id)
    if not item:
        raise exceptions.abort(404, "Item not found")
    return response.json(item)

@app.route("/items", methods=["POST"])
async def add_item(request: Request):
    """
    Add a new item to the inventory.
    """
    try:
        data = request.json
        item_id = str(uuid.uuid4())  # Generate a unique item ID
        inventory[item_id] = data
        return response.json(inventory[item_id], status=201)
    except Exception as e:
        raise exceptions.abort(400, "Invalid data")

@app.route("/items/<item_id:str>", methods=["PUT"])
async def update_item(request: Request, item_id: str):
    """
    Update an existing item in the inventory.
    """
    try:
        data = request.json
        if item_id not in inventory:
            raise exceptions.abort(404, "Item not found")
        inventory[item_id].update(data)
        return response.json(inventory[item_id])
    except Exception as e:
        raise exceptions.abort(400, "Invalid data")

@app.route("/items/<item_id:str>", methods=["DELETE"])
async def delete_item(request: Request, item_id: str):
    """
    Delete an item from the inventory.
    """
    if item_id not in inventory:
        raise exceptions.abort(404, "Item not found")
    del inventory[item_id]
    return response.json({"message": "Item deleted"})

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)